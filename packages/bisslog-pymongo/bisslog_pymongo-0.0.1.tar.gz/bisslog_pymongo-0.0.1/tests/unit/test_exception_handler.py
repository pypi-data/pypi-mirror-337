import pytest
from bson.errors import BSONError
from pymongo.errors import (
    ConnectionFailure, OperationFailure, DuplicateKeyError, CollectionInvalid, ConfigurationError,
    NetworkTimeout, WriteError, PyMongoError
)
from bisslog.exceptions.external_interactions_errors import (
    InvalidDataExtException, IntegrityErrorExtException, ProgrammingErrorExtException,
    ConfigurationExtException, TimeoutExtException, ConnectionExtException,
    OperationalErrorExtException, ExternalInteractionError
)
from bisslog_pymongo import bisslog_exc_mapper_pymongo

# Helper function to simulate a function raising an exception
@bisslog_exc_mapper_pymongo
def function_that_raises(exception):
    raise exception

@pytest.mark.parametrize("exception, expected_exception", [
    (DuplicateKeyError("Duplicate key error"), IntegrityErrorExtException),
    (BSONError("Invalid BSON data"), InvalidDataExtException),
    (CollectionInvalid("Invalid collection"), ProgrammingErrorExtException),
    (ConfigurationError("Configuration issue"), ConfigurationExtException),
    (NetworkTimeout("Network timeout"), TimeoutExtException),
    (WriteError("Write error"), IntegrityErrorExtException),
    (ConnectionFailure("Connection failure"), ConnectionExtException),
    (OperationFailure("Operation failure"), OperationalErrorExtException),
    (PyMongoError("General PyMongo error"), ExternalInteractionError),
])
def test_bisslog_exception_handler_pymongo(exception, expected_exception):
    with pytest.raises(expected_exception):
        function_that_raises(exception)
