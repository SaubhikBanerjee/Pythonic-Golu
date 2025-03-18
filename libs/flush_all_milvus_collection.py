"""
This file will be used to Flush all the Milvus collections
"""
from pymilvus import (Collection, connections, utility)
import sys


def flush_all_milvus_collection():
    try:
        connections.connect("default",
                            host="localhost",
                            server_name="localhost",
                            port=19530,
                            user="root",
                            password='Milvus',
                            secure=True,
                            client_key_path='.\libs\prodtls.key',
                            client_pem_path='.\libs\prodtls.crt',
                            ca_pem_path='.\libs\prodtls.crt',
                            show_startup_banner=True
                            )
        print("Connected to Milvus")
    except Exception as e:
        print("Problem in connecting to Milvus")
        print(e)
        sys.exit(0)
    # Take all the collections into  all_collections
    all_collections = utility.list_collections()
    collection = Collection('GenAIAABolton')
    print(collection)
    # expr_qry = 'chunk_id == "d7a14a48ade648058db828aa10f93c78"'
    expr_qry = 'chunk_id =="Section - d7a14a48ade648058db828aa10f93c78"'
    print(expr_qry)
    res = collection.query(expr=expr_qry, output_fields=["pk"])
    print(res)

    try:
        # for collection in all_collections:
        #     print("Flushing & Compacting collection name: ", collection)
        #
        #     # Loading collection
        #     milvus_collection = Collection(collection)
        #     # Check the loading progress and loading status
        #     print("\033[91m Load state before:\033[00m ", str(utility.load_state(collection)))
        #     if str(utility.load_state(collection)).strip() == "Loaded":
        #         print(utility.loading_progress(collection))
        #         print("Trying to unload...")
        #         milvus_collection.release()
        #         print("\033[92m Load state after:\033[00m ", utility.load_state(collection))
        #     # Flushing collection
        #     #milvus_collection.flush(timeout=None)
        #     # Compacting
        #     # milvus_collection.compact()
        #     # Check the status async.
        #     # milvus_collection.get_compaction_state()
        #
        #     # Releasing the collection
        #     milvus_collection.release()
        #     print("Finished flushing: ", collection)
        print(all_collections)
        print("*" * 40)
    except Exception as e:
        print("Problem in Loading Collection")
        print(e)


if __name__ == '__main__':
    flush_all_milvus_collection()
