#  Python Class for Vector Database Operations

This project implements a simple vector-based document storage and retrieval system using FAISS, Sentence Transformers, and FastAPI. The project supports basic CRUD operations on collections of documents and allows for querying similar documents based on a query text.

## Project Structure
```sh
├── app
│ ├── main.py # FastAPI application
│ ├── vectordb.py # VectorDB implementation
│ ├── vectordb_model.py # VectorDB model implementation
│ ├── vectordb_routes.py # VectorDB routes implementation
│ └── sample_document.txt # Sample document for testing
├── tests
│ └── test_vectordb.py # Unit tests
├── pytest.ini # To run the unit tests
├── vectordb.pkl # Pickle file for saving/loading database state
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
   git clone https://github.com/yourusername/vectordb-fastapi.git
   cd vectordb-fastapi
   
2. **Create and activate a virtual environment**:
   ```sh
   python -m venv venv
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
**Create Collection**: POST /collections/{collection_name}     
**Insert Document**: POST /collections/{collection_name}/documents    
**Update Document**: PUT /collections/{collection_name}/documents/{doc_name}  
**Delete Document**: DELETE /collections/{collection_name}/documents/{doc_name}  
**Retrieve Documents**: POST /collections/{collection_name}/search

### Example Requests
#### Create a Collection:

   ```sh
   curl -X POST "http://127.0.0.1:8000/collections/my_collection"
 ```
   
#### Insert a Document:

   ```sh
   curl -X POST "http://127.0.0.1:8000/collections/my_collection/documents" -H "Content-Type: application/json" -d '{"doc_name": "doc1", "text": "This is a sample document."}'
   ```

#### Update a Document:

   ```sh
   curl -X PUT "http://127.0.0.1:8000/collections/my_collection/documents/doc1" -H "Content-Type: application/json" -d '{"text": "This is an updated document."}'
   ```

#### Delete a Document:

   ```sh
   curl -X DELETE "http://127.0.0.1:8000/collections/my_collection/documents/doc1"
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

### Load the database state:

   ``` sh
   db = VectorDB.load('vectordb.pkl')
   ```

