import os
import pytest
from app.vectordb import VectorDB  # Ensure that the class is properly imported from its module

# Fixture to initialize a VectorDB instance
@pytest.fixture(scope="module")
def vectordb():
    return VectorDB()


# Test function to create a collection
def test_create_collection(vectordb):
    """
    Test the creation of a new collection.
    """
    result = vectordb.create_collection('test_collection', 384)
    assert result == "Collection 'test_collection' created with dimension 384."


# Test function to handle the creation of an existing collection
def test_create_existing_collection(vectordb):
    """
    Test handling the creation of an existing collection.
    """
    with pytest.raises(ValueError, match="Collection 'test_collection' already exists."):
        vectordb.create_collection('test_collection', 384)


# Test function to get the count of collections in the database
def test_get_collection_count(vectordb):
    """
    Test retrieving the count of collections in the database.
    """
    assert vectordb.get_collection_count() == ['test_collection']


# Test function to insert a document into a collection
def test_insert_documents(vectordb):
    """
    Test inserting a document into a collection.
    """
    result = vectordb.insert_documents('test_collection', 'doc1', 'This is a test document.')
    assert result == "Document 'doc1' inserted into collection 'test_collection'."


# Test function to handle the insertion of an existing document
def test_insert_existing_document(vectordb):
    """
    Test handling the insertion of an existing document.
    """
    with pytest.raises(ValueError, match="Document name 'doc1' already exists in the database."):
        vectordb.insert_documents('test_collection', 'doc1', 'This is a test document.')


# Test function to handle insertion into a nonexistent collection
def test_insert_documents_nonexistent_collection(vectordb):
    """
    Test handling insertion into a nonexistent collection.
    """
    with pytest.raises(ValueError, match="Collection 'nonexistent' does not exist."):
        vectordb.insert_documents('nonexistent', 'doc1', 'This is a test document.')


# Test function to retrieve documents based on a query
def test_retrieve_documents(vectordb):
    """
    Test retrieving documents based on a query.
    """
    results = vectordb.retrieve_documents('test_collection', 'test', top_n=1)
    assert len(results) == 1
    assert results[0][0] == 'doc1'


# Test function to update a document in a collection
def test_update_document(vectordb):
    """
    Test updating an existing document in a collection.
    """
    result = vectordb.update_document('test_collection', 'doc1', 'This is an updated document.')
    assert result == "Document 'doc1' in collection 'test_collection' updated."


# Test function to delete a document from a collection
def test_delete_document(vectordb):
    """
    Test deleting a document from a collection.
    """
    result = vectordb.delete_document('test_collection', 'doc1')
    assert result == "Document 'doc1' deleted from collection 'test_collection'."


# Test function to handle updating a nonexistent document
def test_update_nonexistent_document(vectordb):
    """
    Test handling the update of a nonexistent document.
    """
    with pytest.raises(ValueError, match="Document name 'nonexistent' does not exist in the database."):
        vectordb.update_document('test_collection', 'nonexistent', 'This is an updated document.')


# Test function to handle deletion of a nonexistent document
def test_delete_nonexistent_document(vectordb):
    """
    Test handling the deletion of a nonexistent document.
    """
    with pytest.raises(ValueError, match="Document name 'nonexistent' does not exist in the database."):
        vectordb.delete_document('test_collection', 'nonexistent')


# Test function to insert documents from a directory into a collection
def test_insert_documents_from_directory(vectordb):
    """
    Test inserting documents from a directory into a collection.
    """
    directory_path = 'Documents'
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    with open(os.path.join(directory_path, "doc1.txt"), "w") as f:
        f.write("This is document 1.")
    with open(os.path.join(directory_path, "doc2.txt"), "w") as f:
        f.write("This is document 2.")

    vectordb.create_collection('dir_collection', 384)
    result = vectordb.insert_documents_from_directory('dir_collection')
    assert "Inserted 2 documents from 'Documents' into collection 'dir_collection'." in result


# Test function to update documents from a directory in a collection
def test_update_documents_from_directory(vectordb):
    """
    Test updating documents from a directory in a collection.
    """
    directory_path = 'Documents'
    with open(os.path.join(directory_path, "doc1.txt"), "w") as f:
        f.write("This is updated document 1.")
    with open(os.path.join(directory_path, "doc2.txt"), "w") as f:
        f.write("This is updated document 2.")

    result = vectordb.update_documents_from_directory('dir_collection', directory_path)
    assert "Updated 2 documents from 'Documents' in collection 'dir_collection'." in result


# Test function to save and load VectorDB state
def test_save_and_load(vectordb, tmp_path):
    """
    Test saving and loading the VectorDB state.
    """
    # Save the state
    file_path = tmp_path / "vectordb_test.pkl"
    vectordb.save(file_path)

    # Load the state
    loaded_vectordb = VectorDB.load(file_path)
    assert loaded_vectordb.get_collection_count() == vectordb.get_collection_count()
