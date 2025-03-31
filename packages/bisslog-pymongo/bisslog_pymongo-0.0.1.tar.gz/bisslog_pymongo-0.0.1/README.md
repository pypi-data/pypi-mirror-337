# bisslog-pymongo

It is an extension of the bisslog library to support processes with the pymongo driver library of the mongo db database.


## Example usage

~~~python
import os
from pymongo import MongoClient, DESCENDING
from abc import ABC, abstractmethod
from bisslog import Division, bisslog_db
from bisslog_pymongo import BasicPymongoHelper, bisslog_exc_mapper_pymongo


class MarketingDivision(Division, ABC):

    @abstractmethod
    def find_sales_per_client(self, id_client: int):
        raise NotImplementedError("find_sales_per_client must be implemented")


class MarketingMongoDivision(MarketingDivision, BasicPymongoHelper):

    @bisslog_exc_mapper_pymongo
    def find_sales_per_client(self, id_client: int):
        res = self.get_collection("sales").find({"id_client": id_client}).sort(
            {'created_at': DESCENDING})
        return self.stringify_list_identifier(res)


marketing_div = MarketingMongoDivision(MongoClient(os.environ["ATLAS_URI"]),
                                       database_name="marketing")

bisslog_db.register_adapters(marketing=marketing_div)
~~~


## Components

### PymongoHelper

It is just a class that receives the client and has some methods to facilitate the creation of pymongo adapters. the creation of pymongo adapters


### bisslog_exception_handler_pymongo

Decorator to map PyMongo exceptions to their corresponding Bisslog exceptions.


| **Excepción de PyMongo**   | **Excepción de Bisslog**               |
|----------------------------|----------------------------------------|
| `DuplicateKeyError`        | `IntegrityErrorExtException`          |
| `BSONError`               | `InvalidDataExtException`              |
| `CollectionInvalid`       | `ProgrammingErrorExtException`        |
| `ConfigurationError`      | `ConfigurationExtException`           |
| `NetworkTimeout`          | `TimeoutExtException`                 |
| `WriteError`              | `IntegrityErrorExtException`          |
| `ConnectionFailure`       | `ConnectionExtException`              |
| `OperationFailure`        | `OperationalErrorExtException`        |
| `PyMongoError`            | `ExternalInteractionError`            |

### BasicPymongoHelper

`BasicPymongoHelper` is a helper class for interacting with MongoDB databases using PyMongo.  
It provides convenient methods for performing CRUD operations while maintaining traceability through `TransactionTraceable`.



#### **Initialization**
~~~python
BasicPymongoHelper(mongo_client: MongoClient, database_name: str = None)
~~~

Initializes the helper with a `MongoClient` instance.

If database_name is not provided, it uses the default database.

#### **Methods**

- `get_collection`
~~~python
get_collection(collection_name: str, database_name: str = None) -> Collection
~~~
Returns the collection object from the specified database.

If database_name is not provided, it defaults to the instance's database.

- `insert_one`

~~~python
insert_one(collection: str, obj: object = None, *, save_id: bool = False, **kwargs) -> str
~~~

Inserts a document into the specified collection.

If save_id is False, it removes the _id field before insertion.

Returns the inserted document's ID as a string.


- `find_one`

~~~python
find_one(collection: str, query: dict, selection: dict) -> dict
~~~

Retrieves a single document from the specified collection based on query and selection.

Converts the document’s _id to a string before returning.

- `stringify_identifier`

~~~python
@classmethod
stringify_identifier(cls, obj: dict) -> dict
~~~

Converts an ObjectId _id field to a string in a single document.

- `stringify_list_identifier`

~~~python
@classmethod
stringify_list_identifier(cls, list_obj: Iterator) -> list
~~~

Converts the _id field to a string in a list of documents.

- `verify_query`

~~~python
@staticmethod
verify_query(query: dict) -> dict
~~~

Validates and processes a query:

Converts _id field to ObjectId if necessary.

Ensures the query is a dictionary.

Returns None if validation fails.

- `get_length`

~~~python
get_length(collection: str, query: dict) -> int
~~~
   
Returns the number of documents matching the given query in a collection.

