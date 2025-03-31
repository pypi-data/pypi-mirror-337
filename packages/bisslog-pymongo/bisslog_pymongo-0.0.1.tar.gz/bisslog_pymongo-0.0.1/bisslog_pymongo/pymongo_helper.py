"""Pymongo database helper implementation"""
from typing import Iterator

from bson.errors import InvalidId
from bson.objectid import ObjectId

from pymongo import MongoClient
from pymongo.collection import Collection

from bisslog.transactional.transaction_traceable import TransactionTraceable


class BasicPymongoHelper(TransactionTraceable):
    """Helper definition with an approach for mongodb databases with methods predisposed for it"""

    def __init__(self, mongo_client: MongoClient, database_name: str = None) -> None:
        self.client = mongo_client
        if database_name is None:
            self.database = self.client.get_default_database()
        self.database = self.client.get_database(database_name)

    def get_collection(self, collection_name: str, database_name: str=None) -> Collection:
        """Returns the collections object on the database asked"""
        if database_name is None:
            return self.database.get_collection(collection_name)
        return self.client.get_database(database_name).get_collection(collection_name)

    def insert_one(self, collection: str, obj: object = None, *,
                   save_id: bool = False, **kwargs) -> str:
        """Create a document in a collection"""
        if obj is None:
            obj = kwargs
        if not save_id and '_id' in obj:
            del obj['_id']
        insertion_res = self.get_collection(collection).insert_one(obj)
        return str(insertion_res.inserted_id)

    def find_one(self, collection: str, query: dict, selection: dict) -> dict:
        """Get one document from a collection"""
        query = self.verify_query(query)
        res = self.get_collection(collection).find_one(query, selection)
        res = self.stringify_identifier(res)
        return res

    @classmethod
    def stringify_identifier(cls, obj: dict):
        """Convert id from UID to string"""
        if obj is not None and "_id" in obj:
            obj['_id'] = str(obj['_id'])
        return obj

    @classmethod
    def stringify_list_identifier(cls, list_obj: Iterator):
        """Convert a list of unique ID's to string"""
        return list(map(cls.stringify_identifier, list_obj))

    @staticmethod
    def verify_query(query):
        """Verify that the query is valid according to some business rules or techniques."""
        if '_id' in query and query['_id']:
            try:
                query['_id'] = ObjectId(query['_id'])
            except InvalidId:
                return None
        if not isinstance(query, dict):
            return None
        return query

    def get_length(self, collection: str, query: dict) -> int:
        """Get the total number of documents in a collection"""
        return self.get_collection(collection).count_documents(query)
