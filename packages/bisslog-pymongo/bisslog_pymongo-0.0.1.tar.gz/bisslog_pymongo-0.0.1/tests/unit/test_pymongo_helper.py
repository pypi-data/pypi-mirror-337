import pytest
from unittest.mock import MagicMock
from pymongo.collection import Collection
from pymongo.results import InsertOneResult
from bson.objectid import ObjectId

from bisslog_pymongo import BasicPymongoHelper


@pytest.fixture
def mock_mongo_client():
    """Fixture to provide a mock MongoClient."""
    client = MagicMock()
    client.get_database.return_value.get_collection.return_value = MagicMock(spec=Collection)
    return client


@pytest.fixture
def pymongo_helper(mock_mongo_client):
    """Fixture to provide an instance of BasicPymongoHelper with a mocked MongoClient."""
    return BasicPymongoHelper(mock_mongo_client, "test_db")


def test_get_collection(pymongo_helper, mock_mongo_client):
    """Tests if method get_collection returns the correct collection object."""
    collection_name = "test_collection"
    collection = pymongo_helper.get_collection(collection_name)
    assert isinstance(collection, Collection)
    mock_mongo_client.get_database.assert_called_with("test_db")
    mock_mongo_client.get_database().get_collection.assert_called_with(collection_name)


def test_insert_one(pymongo_helper, mock_mongo_client):
    """Test inserting a document into a collection."""
    mock_insert_result = MagicMock(spec=InsertOneResult)
    mock_insert_result.inserted_id = ObjectId()
    mock_mongo_client.get_database().get_collection().insert_one.return_value = mock_insert_result

    inserted_id = pymongo_helper.insert_one("test_collection",
                                            {"test_field1": 245, "test_field2": "Hello", "_id": ObjectId()})

    assert inserted_id == str(mock_insert_result.inserted_id)
    mock_mongo_client.get_database().get_collection().insert_one.assert_called_once()

    inserted_id = pymongo_helper.insert_one(
        "test_collection", {"test_field1": 245, "test_field2": "Hello", "_id": ObjectId()}, save_id=True)
    assert inserted_id == str(mock_insert_result.inserted_id)


def test_find_one(pymongo_helper, mock_mongo_client):
    """Test retrieving a single document from a collection."""
    test_document = {"_id": ObjectId(), "name": "Test Name"}
    expected_document = {"_id": str(test_document["_id"]), "name": "Test Name"}

    mock_mongo_client.get_database().get_collection().find_one.return_value = test_document

    result = pymongo_helper.find_one("test_collection", {"name": "Test Name"}, {})

    assert result == expected_document
    mock_mongo_client.get_database().get_collection().find_one.assert_called_once()


def test_stringify_identifier():
    """Test conversion of ObjectId to string."""
    test_doc = {"_id": ObjectId(), "name": "Test"}
    expected_doc = {"_id": str(test_doc["_id"]), "name": "Test"}
    assert BasicPymongoHelper.stringify_identifier(test_doc) == expected_doc


def test_stringify_list_identifier():
    """Test conversion of a list of documents' ObjectIds to strings."""
    test_docs = [{"_id": ObjectId(), "name": "Test1"}, {"_id": ObjectId(), "name": "Test2"}]
    expected_docs = [{"_id": str(doc["_id"]), "name": doc["name"]} for doc in test_docs]
    assert BasicPymongoHelper.stringify_list_identifier(test_docs) == expected_docs


def test_verify_query():
    """Test query verification and ObjectId conversion."""
    valid_query = {"_id": str(ObjectId())}
    processed_query = BasicPymongoHelper.verify_query(valid_query)
    assert isinstance(processed_query["_id"], ObjectId)

    invalid_query = {"_id": "invalid_object_id"}
    assert BasicPymongoHelper.verify_query(invalid_query) is None

    non_dict_query = "not a dict"
    assert BasicPymongoHelper.verify_query(non_dict_query) is None


def test_get_length(pymongo_helper, mock_mongo_client):
    """Test getting the count of documents in a collection."""
    mock_mongo_client.get_database().get_collection().count_documents.return_value = 5
    count = pymongo_helper.get_length("test_collection", {})
    assert count == 5
    mock_mongo_client.get_database().get_collection().count_documents.assert_called_once()
