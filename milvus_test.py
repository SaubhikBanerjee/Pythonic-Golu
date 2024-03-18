from pymilvus import (Collection, FieldSchema, CollectionSchema,
                      DataType, connections, utility)
import sys
import random
import string


def connect_to_milvus(connection_alias):
    try:
        connections.connect(connection_alias, host="localhost", port=19530)
        print("Connected to Milvus")
        return connection_alias
    except Exception as e:
        print("Problem in connecting to Milvus")
        print(e)
        sys.exit(0)


def create_milvus_collection(collection_name, connection_alias):
    try:

        if utility.has_collection(collection_name):
            utility.drop_collection(collection_name)

        # Step 1: Creating 3 Field Schema
        song_name = FieldSchema(
            name="song_name",
            dtype=DataType.VARCHAR,
            max_length=200,
        )
        song_id = FieldSchema(
            name="song_id",
            dtype=DataType.INT64,
            is_primary=True,
        )
        listen_count = FieldSchema(
            name="listen_count",
            dtype=DataType.INT64,
        )
        song_vec = FieldSchema(
            name="song_vec",
            dtype=DataType.FLOAT_VECTOR,
            dim=2
        )
        # Step 2: Collection schema
        collection_schema = CollectionSchema(
            fields=[song_name, song_id, listen_count, song_vec],
            description="Album Songs"
        )
        # Step 3: Create collection
        collection = Collection(
            name=collection_name,
            schema=collection_schema,
            using=connection_alias)
        return collection
    except Exception as e:
        print(e)


def release_milvus_collection(collection_alias):
    collection_alias.release()


def create_milvus_partition(collection_alias, partition_name):
    if not collection_alias.has_partition(partition_name):
        collection_alias.create_partition(partition_name)
    else:
        print("Partition already exists!")


def create_vector_index(collection_alias, field_name, index_params):
    collection_alias.create_index(field_name, index_params)


def create_scalar_index(collection_alias, field_name, index_name):
    collection_alias.create_index(field_name, index_name)


def insert_collection_data(collection_alias, _data):
    data_insert = collection_alias.insert(_data)
    collection_alias.flush()

    # collection_alias.compact()
    # print(collection_alias.get_compaction_state())


def get_milvus_collection_details(collection_alias):
    print("Schema: ", collection_alias.schema)
    print("Description: ", collection_alias.description)
    print("Name: ", collection_alias.name)
    print("Empty?: ", collection_alias.is_empty)
    print("Entities: ", collection_alias.num_entities)
    print("Primary Key: ", collection_alias.primary_field)
    print("Partitions: ", collection_alias.partitions)
    print("Indexes: ", collection_alias.indexes)
    print("Properties:", collection_alias.properties)


if __name__ == '__main__':
    milvus_connection = connect_to_milvus("default")
    print("Collections: ", utility.list_collections())
    milvus_collection = create_milvus_collection("SongAlbum", milvus_connection)
    print("Collections: ", utility.list_collections())
    create_milvus_partition(milvus_collection, "Partition1")
    create_milvus_partition(milvus_collection, "Partition2")
    get_milvus_collection_details(milvus_collection)
    # Prepare data to be inserted
    num_entities = 5
    data = [
        [''.join(random.choices(string.ascii_uppercase, k=7)) for i in range(num_entities)],  # song name
        [i for i in range(num_entities)],  # Song ID
        [random.randint(0, 100000) for i in range(num_entities)],  # Listen Count
        [[random.random() for _ in range(2)] for _ in range(num_entities)]  # song_vec - 2d vector
    ]
    insert_collection_data(milvus_collection, data)
    get_milvus_collection_details(milvus_collection)

    # Create Index
    index_params = {
        "metric_type": "L2",
        "index_type": "IVF_FLAT",
        "params": {"nlist":1024},
        "index_name": "Custom_IVF"
    }
    create_vector_index(milvus_collection, "song_vec", index_params)
    create_scalar_index(milvus_collection, "song_name",  "scalar_index_Album1")

    # Query the data in scalar field
    # Load the collection in to the memory
    milvus_collection.load(replica_number=1)

    query_res = milvus_collection.query(
        expr="song_id > 0",
        limit=10,
        output_fields=["song_name", "listen_count"]
    )

    for result in query_res:
        print(result)
    release_milvus_collection(collection_alias=milvus_collection)
    connections.disconnect(milvus_connection)
