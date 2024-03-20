"""
This files contains various utility functions to create collections, indexes etc
"""
from pymilvus import (Collection, FieldSchema, CollectionSchema,
                      DataType, connections, utility)
import sys
# Make it lib.read_config after unit testing.
from libs.read_config import ReadConfig


def connect_to_milvus(connection_alias):
    try:
        my_config = ReadConfig("config/config.ini")
        # Connecting to my local Milvus in docker image.
        connections.connect(connection_alias,
                            host=my_config.host,
                            port=my_config.port
                            )
        print("Connected to Milvus!")
        # Check if the server is ready.
        print("Database Version: ", utility.get_server_version())
        return connection_alias
    except Exception as e:
        print("Problem in connecting to Milvus")
        print(e)
        sys.exit(0)


def create_milvus_collection(collection_name, connection_alias):
    try:
        # If collection exists we are dropping it.
        if utility.has_collection(collection_name):
            utility.drop_collection(collection_name)

        # Step 1: Creating 3 Field Schema
        question_id = FieldSchema(
            name="question_id",
            dtype=DataType.INT64,
            is_primary=True,
        )
        question = FieldSchema(
            name="question",
            dtype=DataType.VARCHAR,
            max_length=65535,
        )
        answer = FieldSchema(
            name="answer",
            dtype=DataType.VARCHAR,
            max_length=65535
        )
        reference = FieldSchema(
            name="reference",
            dtype=DataType.VARCHAR,
            max_length=500
        )

        question_vec = FieldSchema(
            name="question_vec",
            dtype=DataType.FLOAT_VECTOR,
            dim=768
        )
        # Step 2: Collection schema
        collection_schema = CollectionSchema(
            fields=[question_id, question, answer, reference, question_vec],
            description="Python Question Answer"
        )
        # Step 3: Create collection
        collection = Collection(
            name=collection_name,
            schema=collection_schema,
            using=connection_alias,
            consistency_level="Strong"
        )
        return collection
    except Exception as e:
        print(e)


def create_milvus_collection_v2(collection_name, connection_alias):
    my_config = ReadConfig("config/config.ini")
    try:
        # If collection exists we are dropping it.
        if utility.has_collection(collection_name):
            utility.drop_collection(collection_name)

        # Step 1: Creating 3 Field Schema
        book_chunk_id = FieldSchema(
            name="book_chunk_id",
            dtype=DataType.VARCHAR,
            max_length=2000,
            is_primary=True,
        )
        book_name = FieldSchema(
            name="book_name",
            dtype=DataType.VARCHAR,
            max_length=2000,
        )
        book_author = FieldSchema(
            name="book_author",
            dtype=DataType.VARCHAR,
            max_length=1000
        )
        book_chunk = FieldSchema(
            name="book_chunk",
            dtype=DataType.VARCHAR,
            max_length=65535
        )

        book_chunk_vec = FieldSchema(
            name="book_chunk_vec",
            dtype=DataType.FLOAT_VECTOR,
            dim=my_config.vector_dim
        )
        # Step 2: Collection schema
        collection_schema = CollectionSchema(
            fields=[book_chunk_id, book_name, book_author, book_chunk, book_chunk_vec],
            description="Python Books"
        )
        # Step 3: Create collection
        collection = Collection(
            name=collection_name,
            schema=collection_schema,
            using=connection_alias,
            consistency_level="Strong"
        )
        return collection
    except Exception as e:
        print(e)


def disconnect_from_milvus(connection_alias):
    connections.disconnect(connection_alias)
    print("Disconnected from Milvus!")


def create_vector_index(collection_alias, field_name, index_params):
    collection_alias.create_index(field_name, index_params)


def create_scalar_index(collection_alias, field_name, index_name):
    collection_alias.create_index(field_name, index_name)


if __name__ == '__main__':
    # Connect to Milvus
    milvus_connection = connect_to_milvus("default")
    milvus_collection = create_milvus_collection("PythonQA", milvus_connection)
    milvus_collection_v2 = create_milvus_collection_v2("PythonBooks", milvus_connection)
    print("Collections: ", utility.list_collections())
    disconnect_from_milvus(milvus_connection)




