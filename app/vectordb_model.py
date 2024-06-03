from pydantic import BaseModel


class Document(BaseModel):
    """
    Pydantic model representing a document to be inserted into a collection.
    Attributes:
        doc_name (str): The unique name of the document.
        text (str): The text content of the document.
    """
    doc_name: str
    text: str

class Query(BaseModel):
    """
    Pydantic model representing a query for retrieving documents from a collection.
    Attributes:
        query (str): The search query text.
        top_n (int, optional): The number of top results to return. Default is 5.
    """
    query: str
    top_n: int = 5

class Collection(BaseModel):
    """
    Pydantic model representing a collection to be created in the database.
    Attributes:
        name (str): The name of the collection.
        dimension (int, optional): The dimensionality of the collection's index. Default is 384.
    """
    name: str
    dimension: int = 384
