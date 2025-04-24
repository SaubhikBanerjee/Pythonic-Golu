"""
This file will be used to Flush all the Milvus collections
"""
from pymilvus import (Collection, connections, utility)
import sys


def load_milvus_collection():
    try:
        connections.connect("default",
                            host="localhost",
                            server_name="localhost",
                            port=19530,
                            user="root",
                            password='Milvus',
                            secure=True,
                            client_key_path='.\\Certs\\aiopsdev3tls.key',
                            client_pem_path='.\\Certs\\aiopsdev3tls.crt',
                            ca_pem_path='.\\Certs\\aiopsdev3tls.crt',
                            show_startup_banner=True
                            )
        print("Connected to Milvus")
        print("Database Version:", utility.get_server_version())
    except Exception as e:
        print("Problem in connecting to Milvus")
        print(e)
        sys.exit(0)
    # Take all the collections into  all_collections
    all_collections = utility.list_collections()

    try:
        for collection in all_collections:
            # print("Loading & Flushing collection name: ", collection)

            # Loading collection
            # milvus_collection = Collection(collection)
            # Check the loading progress and loading status
            # print(milvus_collection.schema)
            # print(milvus_collection.indexes)
            print("\033[91m Load state:\033[00m ", str(utility.load_state(collection)))
            if str(utility.load_state(collection)).strip() == "Loaded":
                print("Loaded:", utility.loading_progress(collection))
                print("Trying to unload...")
                # milvus_collection.release()
                print("\033[92m Load state after:\033[00m ", utility.load_state(collection))
            # Flushing collection
            # milvus_collection.flush(timeout=None)
        #     # Compacting
        #     # milvus_collection.compact()
        #     # Check the status async.
        #     # milvus_collection.get_compaction_state()
        #
        #     # Releasing the collection
        #     milvus_collection.release()
        #     print("Finished flushing: ", collection)
    except Exception as e:
        print("Problem in Loading Collection")
        print(e)


if __name__ == '__main__':
    load_milvus_collection()
