import os
import pickle
import warnings
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Suppress specific warnings to avoid unnecessary console output
warnings.filterwarnings("ignore", message="Found Intel OpenMP")
warnings.filterwarnings("ignore", message="`huggingface_hub` cache-system uses symlinks")
warnings.filterwarnings("ignore", category=FutureWarning)

class VectorDB:
    def __init__(self, model_name='paraphrase-MiniLM-L6-v2'):
        """
        Initialize the VectorDB with a SentenceTransformer model.
        """
        self.model = SentenceTransformer(model_name)
        self.collections = {}  # Dictionary to store collections
        self.doc_name_map = {}  # Mapping of document names to their text

    def create_collection(self, collection_name, dimension):
        """
        Create a new collection with a specified dimension for the index.
        """
        if collection_name in self.collections:
            raise ValueError(f"Collection '{collection_name}' already exists.")

        # Create a FAISS index with L2 distance metric
        index = faiss.IndexFlatL2(dimension)
        self.collections[collection_name] = {
            'index': index,
            'vectors': [],
            'doc_names': []
        }
        return f"Collection '{collection_name}' created with dimension {dimension}."

    def get_collection_count(self):
        """
        Returns the list of collection names.
        """
        return list(self.collections.keys())

    def insert_document(self, collection_name, doc_name, text):
        """
        Insert a new document into a specified collection.
        """
        if collection_name not in self.collections:
            raise ValueError(f"Collection '{collection_name}' does not exist.")
        if doc_name in self.doc_name_map:
            raise ValueError(f"Document name '{doc_name}' already exists in the database.")

        # Encode the document text into a vector
        vector = self.model.encode([text])[0]
        collection = self.collections[collection_name]
        collection['index'].add(np.array([vector], dtype=np.float32))
        collection['vectors'].append(vector)
        collection['doc_names'].append(doc_name)
        self.doc_name_map[doc_name] = text
        return f"Document '{doc_name}' inserted into collection '{collection_name}'."

    def update_document(self, collection_name, doc_name, new_text):
        """
        Update an existing document in a specified collection.
        """
        if collection_name not in self.collections:
            raise ValueError(f"Collection '{collection_name}' does not exist.")
        if doc_name not in self.doc_name_map:
            raise ValueError(f"Document name '{doc_name}' does not exist in the database.")

        collection = self.collections[collection_name]
        idx = collection['doc_names'].index(doc_name)

        # Encode the new document text into a vector
        new_vector = self.model.encode([new_text])[0]
        collection['index'].remove_ids(np.array([idx], dtype=np.int64))
        collection['index'].add(np.array([new_vector], dtype=np.float32))

        collection['vectors'][idx] = new_vector
        self.doc_name_map[doc_name] = new_text
        return f"Document '{doc_name}' in collection '{collection_name}' updated."

    def delete_document(self, collection_name, doc_name):
        """
        Delete a document from a specified collection.
        """
        if collection_name not in self.collections:
            raise ValueError(f"Collection '{collection_name}' does not exist.")
        if doc_name not in self.doc_name_map:
            raise ValueError(f"Document name '{doc_name}' does not exist in the database.")

        collection = self.collections[collection_name]
        idx = collection['doc_names'].index(doc_name)

        collection['index'].remove_ids(np.array([idx], dtype=np.int64))
        collection['vectors'].pop(idx)
        collection['doc_names'].remove(doc_name)
        del self.doc_name_map[doc_name]
        return f"Document '{doc_name}' deleted from collection '{collection_name}'."

    def retrieve_documents(self, collection_name, query, top_n=5):
        """
        Retrieve the top N documents from a specified collection based on a query.
        """
        if collection_name not in self.collections:
            raise ValueError(f"Collection '{collection_name}' does not exist.")

        collection = self.collections[collection_name]

        if len(collection['doc_names']) == 0:
            return []
        top_n = min(top_n, len(collection['doc_names']))

        # Encode the query text into a vector
        query_vector = self.model.encode([query])[0]
        distances, indices = collection['index'].search(np.array([query_vector], dtype=np.float32), top_n)

        results = []
        for idx in indices[0][:top_n]:
            if idx < len(collection['doc_names']):
                doc_name = collection['doc_names'][idx]
                results.append((doc_name, self.doc_name_map[doc_name]))

        return results

    def save(self, file_path='vectordb.pkl'):
        """
        Save the current state of the VectorDB to a file.
        """
        with open(file_path, 'wb') as file:
            pickle.dump(self, file)

    @staticmethod
    def load(file_path='vectordb.pkl'):
        """
        Load the VectorDB state from a file.
        """
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                return pickle.load(file)
        else:
            return VectorDB()
