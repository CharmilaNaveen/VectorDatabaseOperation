from fastapi import FastAPI, HTTPException
from app.vectordb import VectorDB
from app.vectordb_model import Collection, Document, Query

# Initialize the FastAPI app
app = FastAPI()
# Load the VectorDB instance from the default file
db = VectorDB.load()

@app.post("/collections/")
def create_collection(collection: Collection):
    """
    Endpoint to create a new collection.
    """
    try:
        db.create_collection(collection.name, collection.dimension)
        db.save()
        return {"message": f"Collection '{collection.name}' created."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/count_collection")
def get_collections():
    """
    Endpoint to get the count of collections in the database.
    """
    return db.get_collection_count()

@app.post("/collections/{collection_name}/documents/")
def insert_document(collection_name: str, document: Document):
    """
    Endpoint to insert a new document into a collection.
    """
    try:
        db.insert_document(collection_name, document.doc_name, document.text)
        db.save()
        return {"message": f"Document '{document.doc_name}' inserted into collection '{collection_name}'."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/collections/{collection_name}/documents/{doc_name}")
def update_document(collection_name: str, doc_name: str, new_text: str):
    """
    Endpoint to update an existing document in a collection.
    """
    try:
        db.update_document(collection_name, doc_name, new_text)
        db.save()
        return {"message": f"Document '{doc_name}' in collection '{collection_name}' updated."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/collections/{collection_name}/documents/{doc_name}")
def delete_document(collection_name: str, doc_name: str):
    """
    Endpoint to delete a document from a collection.
    """
    try:
        db.delete_document(collection_name, doc_name)
        db.save()
        return {"message": f"Document '{doc_name}' deleted from collection '{collection_name}'."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/collections/{collection_name}/search/")
def retrieve_documents(collection_name: str, query: Query):
    """
    Endpoint to retrieve documents from a collection based on a query.
    """
    try:
        results = db.retrieve_documents(collection_name, query.query, query.top_n)
        return {"results": results}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/save/")
def save_db():
    """
    Endpoint to manually save the current state of the database to a file.
    """
    db.save()
    return {"message": "VectorDB state saved."}

@app.post("/load/")
def load_db():
    """
    Endpoint to manually load the state of the database from a file.
    """
    global db
    db = VectorDB.load()
    return {"message": "VectorDB state loaded."}
