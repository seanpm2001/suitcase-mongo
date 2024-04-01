# This separate fixtures module allows external libraries (e.g.
# intake-bluesky-mongo) to import and reuse this fixtures without importing
# *all* the fixtures used in conftest and the dependencies that they carry.
import mongomock
import pytest
import uuid
from suitcase.mongo_normalized import Serializer


@pytest.fixture()
def db_factory_no_indexes(request):
    def inner():
        database_name = f'test-{str(uuid.uuid4())}'
        uri = 'mongodb://localhost:27017/'
        client = mongomock.MongoClient(uri)
        db = client[database_name]

        def drop():
            client.drop_database(database_name)

        request.addfinalizer(drop)
        return db
    return inner


@pytest.fixture()
def db_factory(request):
    def inner():
        database_name = f'test-{str(uuid.uuid4())}'
        uri = 'mongodb://localhost:27017/'
        client = mongomock.MongoClient(uri)
        db = client[database_name]
        serializer = Serializer(db, db)
        serializer.create_indexes()

        def drop():
            client.drop_database(database_name)

        request.addfinalizer(drop)
        return db
    return inner
