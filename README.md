#  Python Class for Vector Database Operations

This project implements a simple vector-based document storage and retrieval system using FAISS, Sentence Transformers, and FastAPI. The project supports basic CRUD operations on collections of documents and allows for querying similar documents based on a query text.

## Project Structure
```sh
├── app
│ ├── Documents
│ │ └── sample_document.txt # Sample Document for Crud Operation
│ ├── main.py # FastAPI application
│ ├── vectordb.pkl # Pickle file for saving/loading database state
│ ├── vectordb.py # VectorDB implementation
│ ├── vectordb_model.py # VectorDB model implementation
│ ├── vectordb_routes.py # VectorDB routes implementation
├── tests
│ ├── Documents
│ │ └── doc1.txt # Sample Document1 for testing Crud Operation
│ │ └── doc2.txt # Sample Document2 for testing Crud Operation
│ └── test_vectordb.py # Unit tests
├── pytest.ini # To run the unit tests
├── requirements.txt # Project dependencies
└── README.md # This file
```



## Setup

### Prerequisites

- Python 3.7+
- pip (Python package installer)

### Installation

1. **Clone the repository**:
   ```sh
   git clone <repository-url>
   
2. **Create and activate a virtual environment**:
   ```sh
   python -m venv 
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. **Install the required packages**:
   ```sh
   pip install -r requirements.txt
   

### Running the Application
1. **Start the FastAPI server**:

   ```sh
   python main.py
   
   
2. **Access the API documentation**:
Open your web browser and navigate to http://127.0.0.1:8000/docs to view and interact with the API.


### Usage
#### Endpoints
**Create Collection**: POST /create_collections     
**Insert Document**: POST /insert_documents_from_directory    
**Update Document**: PUT /update_documents_from_directory 
**Delete Document**: DELETE /collections/{collection_name}/documents/{doc_name}  
**Retrieve Documents**: POST /collections/{collection_name}/search

### Example Requests
#### Create a Collection:

   ```sh
curl -X 'POST' \
  'http://localhost:8000/collections/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Collection_name",
  "dimension": 384
}'
 ```
   
   
#### Insert a Document:

   ```sh
curl -X 'POST' \
  'http://localhost:8000/insert_documents_from_directory' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "collection_name": "collection_name"
}'
  ```

#### Update a Document:

   ```sh
curl -X 'PUT' \
  'http://localhost:8000/update_documents_from_directory' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "collection_name": "collection_name"
}'
   ```

#### Delete a Document:

   ```sh
curl -X 'DELETE' \
  'http://localhost:8000/collections/{collection_name}/documents/{document_name}' \
  -H 'accept: application/json'
  ```

#### Retrieve Documents:

   ```sh
   curl -X GET "http://127.0.0.1:8000/collections/my_collection/search?query=sample&top_n=5"
   ```

## Testing
This project uses pytest for unit testing. The tests cover the main functionalities of the VectorDB class.

### Running Tests
#### Install pytest:

   ```sh
   pip install pytest 
   ```

#### Run the tests:

   ```sh
   pytest
   ```

### Sample Document
A sample document (sample_document.txt) is provided in the app directory for testing purposes. You can use this document to test the insertion and retrieval functionalities.

### Saving and Loading Database State
The VectorDB class includes methods for saving the state to a file (vectordb.pkl) and loading it from a file. This allows you to persist the state of the database across sessions.

### Save the database state:

   ```sh
   db.save('vectordb.pkl')
   ```



