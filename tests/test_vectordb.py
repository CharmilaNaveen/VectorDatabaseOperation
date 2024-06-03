import os
import pytest
from app.vectordb import VectorDB


@pytest.fixture
def db():
    """
    Fixture to provide a fresh instance of VectorDB for each test.
    Removes the existing pickle file to ensure no state is carried over between tests.
    """
    if os.path.exists('vectordb.pkl'):
        os.remove('vectordb.pkl')
    return VectorDB()


def test_create_collection(db):
    """
    Test to verify collection creation.
    Ensures that a collection is added to the database and initialized correctly.
    """
    db.create_collection('test_collection')
    assert 'test_collection' in db.collections
    assert db.collections['test_collection']['index'].d == 384


def test_insert_document(db):
    """
    Test to verify document insertion into a collection.
    Checks that the document is correctly mapped and stored within the collection.
    """
    db.create_collection('test_collection')
    text = "This is a sample document."
    db.insert_document('test_collection', 'doc_1', text)
    assert 'doc_1' in db.doc_name_map
    assert len(db.collections['test_collection']['doc_names']) == 1
    assert db.collections['test_collection']['doc_names'][0] == 'doc_1'


def test_update_document(db):
    """
    Test to verify updating an existing document in a collection.
    Ensures the document content is updated correctly in the document name map.
    """
    db.create_collection('test_collection')
    text = "This is a sample document."
    db.insert_document('test_collection', 'doc_1', text)
    new_text = "This is an updated document."
    db.update_document('test_collection', 'doc_1', new_text)
    assert db.doc_name_map['doc_1'] == new_text


def test_delete_document(db):
    """
    Test to verify deletion of a document from a collection.
    Ensures the document is removed from both the document name map and the collection's document names list.
    """
    db.create_collection('test_collection')
    text = "This is a sample document."
    db.insert_document('test_collection', 'doc_1', text)
    db.delete_document('test_collection', 'doc_1')
    assert 'doc_1' not in db.doc_name_map
    assert len(db.collections['test_collection']['doc_names']) == 0


def test_retrieve_documents(db):
    """
    Test to verify document retrieval based on a query.
    Ensures the correct documents are retrieved and ranked according to relevance.
    """
    db.create_collection('test_collection')
    text1 = "This is the first sample document."
    text2 = "This is the second sample document."
    db.insert_document('test_collection', 'doc_1', text1)
    db.insert_document('test_collection', 'doc_2', text2)
    results = db.retrieve_documents('test_collection', 'first', top_n=1)
    assert len(results) == 1
    assert results[0][0] == 'doc_1'
    assert results[0][1] == text1


def test_save_load_db(db):
    """
    Test to verify saving the state of the database to a file and loading it back.
    Ensures that the database state is correctly persisted and restored.
    """
    db.create_collection('test_collection')
    text = "This is a sample document."
    db.insert_document('test_collection', 'doc_1', text)
    db.save('vectordb_test.pkl')

    loaded_db = VectorDB.load('vectordb_test.pkl')
    assert 'test_collection' in loaded_db.collections
    assert 'doc_1' in loaded_db.doc_name_map
    assert loaded_db.doc_name_map['doc_1'] == text
