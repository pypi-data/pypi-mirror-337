"""bisslog_exception_handler_pymongo decorator implementation"""
from functools import wraps

from bisslog.exceptions.external_interactions_errors import (
    InvalidDataExtException, IntegrityErrorExtException, ProgrammingErrorExtException,
    ConfigurationExtException, TimeoutExtException, ConnectionExtException,
    OperationalErrorExtException, ExternalInteractionError
)

from bson.errors import BSONError
from pymongo.errors import (
    ConnectionFailure, OperationFailure, DuplicateKeyError, CollectionInvalid,
    ConfigurationError, NetworkTimeout, WriteError, PyMongoError
)


def bisslog_exc_mapper_pymongo(func):
    """Decorator to catch and log specific PyMongo exceptions."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except DuplicateKeyError as error:
            raise IntegrityErrorExtException from error

        except BSONError as error:
            raise InvalidDataExtException from error

        except CollectionInvalid as error:
            raise ProgrammingErrorExtException from error

        except ConfigurationError as error:
            raise ConfigurationExtException from error

        except NetworkTimeout as error:
            raise TimeoutExtException from error

        except WriteError as error:
            raise IntegrityErrorExtException from error

        except ConnectionFailure as error:
            raise ConnectionExtException from error

        except OperationFailure as error:
            raise OperationalErrorExtException from error

        except PyMongoError as error:
            raise ExternalInteractionError from error

    return wrapper
