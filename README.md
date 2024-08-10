# Image-Based Search Engine

## Overview

The Image-Based Search Engine project allows users to upload images, which are then analyzed for descriptive tags using Azure's Computer Vision service. The system searches for similar images in an Azure Search Index and displays results, including images and their descriptions, to the user.

## Features

- Upload images via a web interface.
- Analyze images using Azure Computer Vision to extract descriptive tags.
- Search for similar images stored in an Azure Search Index.
- Display similar images with their descriptions.

## Technologies

- **Azure Blob Storage**: For storing uploaded images.
- **Azure Computer Vision**: For image analysis and tag extraction.
- **Azure Search**: For indexing and searching similar images.
- **Flask**: Web framework for creating the server-side application.
- **HTML/CSS/JavaScript**: For the frontend interface.

## Prerequisites

1. **Azure Account**: You'll need an Azure account with access to Azure Blob Storage, Azure Computer Vision, and Azure Search services.
2. **Python**: Ensure Python 3.6 or higher is installed on your machine.
3. **Flask**: Install Flask for running the web server.
4. **Azure SDKs**: Install the necessary Azure SDK packages for Python.

## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/joery0x3b800001/Image-Based-Search-Engine.git
    cd Image-Based-Search-Engine
    ```

2. **Create and Activate a Virtual Environment**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**

    Create a `requirements.txt` file with the following content:

    ```
    flask
    azure-search-documents
    azure-cognitiveservices-vision-computervision
    azure-storage-blob
    azure-cosmos
    python-dotenv
    ```

    Then, install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1. **Set Up Azure Services**

    - **Azure Blob Storage**: Create a container named `my-container`.
    - **Azure Computer Vision**: Create a Computer Vision resource and get the API key and endpoint.
    - **Azure Search**: Create an Azure Search service, set up an index with fields `imageUrl` and `description`, and get the API key.

2. **Update Configuration**

    Edit the `app.py` file to include your Azure credentials:

    ```python
    AZURE_BLOB_CONNECTION_STRING = 'your_blob_connection_string'
    AZURE_COMPUTER_VISION_KEY = 'your_computer_vision_key'
    AZURE_COMPUTER_VISION_ENDPOINT = 'your_computer_vision_endpoint'
    AZURE_SEARCH_SERVICE_NAME = 'your_search_service_name'
    AZURE_SEARCH_API_KEY = 'your_search_api_key'
    AZURE_SEARCH_INDEX_NAME = 'your_search_index_name'
    ```

## Index Description for Azure Search

Here's an example index description for Azure Search based on the document structure:

```json
{
  "name": "myindex",
  "fields": [
    {
      "name": "id",
      "type": "Edm.String",
      "key": true,
      "filterable": false,
      "sortable": false,
      "facetable": false,
      "searchable": false
    },
    {
      "name": "imageUrl",
      "type": "Edm.String",
      "key": false,
      "filterable": true,
      "sortable": false,
      "facetable": false,
      "searchable": false
    },
    {
      "name": "tags",
      "type": "Collection(Edm.String)",
      "key": false,
      "filterable": true,
      "sortable": false,
      "facetable": true,
      "searchable": true
    }
  ]
}
```

## Running the Application

1. **Initialize the Search Index**

    Run the application once to create or update the Azure Search index:

    ```bash
    python app.py
    ```

2. **Open the Web Interface**

    Open your web browser and navigate to `http://127.0.0.1:5000`. You can now upload images and search for similar images.

## Usage

1. **Upload an Image**

    Use the file input to choose an image file from your device and click the "Upload" button.

2. **View Results**

    After uploading, the page will display the extracted tags and similar images found in the search index.

## Troubleshooting

- **Error initializing Azure clients**: Ensure that your Azure credentials are correctly set in `app.py` and that the Azure services are properly configured.
- **No similar images found**: Make sure that your Azure Search index is correctly populated with images and descriptions.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE.md) file for details.

---

Feel free to adjust any section as needed based on your specific requirements or changes in the project.