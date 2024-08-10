from flask import Flask, request, jsonify, render_template
from azure.storage.blob import BlobServiceClient
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import SearchMode
from msrest.authentication import CognitiveServicesCredentials
from dotenv import load_dotenv
import os
import uuid  # For generating unique keys

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv(os.getenv())

# Azure credentials from environment variables
AZURE_BLOB_CONNECTION_STRING = os.getenv('AZURE_BLOB_CONNECTION_STRING')
AZURE_COMPUTER_VISION_KEY = os.getenv('AZURE_COMPUTER_VISION_KEY')
AZURE_COMPUTER_VISION_ENDPOINT = os.getenv('AZURE_COMPUTER_VISION_ENDPOINT')
AZURE_SEARCH_SERVICE_NAME = os.getenv('AZURE_SEARCH_SERVICE_NAME')
AZURE_SEARCH_API_KEY = os.getenv('AZURE_SEARCH_API_KEY')
AZURE_SEARCH_INDEX_NAME = os.getenv('AZURE_SEARCH_INDEX_NAME')

# Initialize Azure clients
credentials = CognitiveServicesCredentials(AZURE_COMPUTER_VISION_KEY)
blob_service_client = BlobServiceClient.from_connection_string(AZURE_BLOB_CONNECTION_STRING)
vision_client = ComputerVisionClient(AZURE_COMPUTER_VISION_ENDPOINT, credentials=credentials)
search_client = SearchClient(endpoint=f'https://{AZURE_SEARCH_SERVICE_NAME}.search.windows.net/',
                             index_name=AZURE_SEARCH_INDEX_NAME,
                             credential=AzureKeyCredential(AZURE_SEARCH_API_KEY))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    blob_name = file.filename
    blob_client = blob_service_client.get_blob_client(container='my-container', blob=blob_name)

    # Upload new image with overwrite option
    try:
        blob_client.upload_blob(file, overwrite=True)
    except Exception as e:
        return jsonify({'error': f'Blob upload error: {str(e)}'})

    # Extract features from image
    image_url = blob_client.url
    print(f"Uploaded Image URL: {image_url}")
    try:
        features = vision_client.analyze_image(image_url, visual_features=[VisualFeatureTypes.tags])
        tags = [tag.name for tag in features.tags] if features.tags else []
        
    except Exception as e:
        return jsonify({'error': f'Image analysis error: {str(e)}'})
    
    # Generate a unique document key
    document_key = str(uuid.uuid4())

    # Prepare the document
    document = {
        "id": document_key,
        "imageUrl": image_url,
        "tags": tags
    }

    # Upload document to the search index
    try:
        result = search_client.upload_documents(documents=[document])
        print(f"Documents uploaded: {result}")
    except Exception as e:
        print(f"Error uploading documents: {e}")

    # Search for images with similar tags
    try:
        search_results = search_client.search(search_text="*", search_mode=SearchMode.ALL)

        matched_images = []
        for result in search_results:
            result_tags = result.get('tags', [])
            url = result.get('imageUrl', '')
            if any(tag in tags for tag in result_tags):
                matched_images.append(url)

        if not matched_images:
            matched_images = ['No similar images found']

    except Exception as e:
        return jsonify({'error': f'Search error: {str(e)}'})

    return jsonify({'tags': tags, 'similar_images': matched_images})

if __name__ == '__main__':
    app.run(debug=True)
