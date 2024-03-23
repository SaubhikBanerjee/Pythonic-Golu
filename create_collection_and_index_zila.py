"""
This file used to create two main collections used in the application. Those are
1. PythonQA
2. PythonBooks
This file is also used to create required indexes on the collection.
"""
# Good Reads: https://github.com/christy/ZillizDemos/blob/main/milvus_onboarding/hello_world_milvus.ipynb

from libs import (connect_to_milvus_zila,
                  create_milvus_collection,
                  create_milvus_collection_v2,
                  create_vector_index,
                  disconnect_from_milvus
                  )
from pymilvus import utility

if __name__ == '__main__':
    # Connect to Milvus
    milvus_connection = connect_to_milvus_zila("default")
    # Create collection named PythonQA
    milvus_collection = create_milvus_collection("PythonQA", milvus_connection)
    # Create collection named PythonBooks
    milvus_collection_v2 = create_milvus_collection_v2("PythonBooks", milvus_connection)
    print("Collections: ", utility.list_collections())
    # Create Index on PythonQA
    index_params = {
        "metric_type": "COSINE",
        "index_type": "HNSW",
        "params": {"M": 16,  # int. 4~64, num_neighbors, higher values takes more memory.
                   "efConstruction": 32  # int. 8~512, num_candidate_nearest_neighbors
                   },
        "index_name": "PythonQA_HNSW"
    }
    create_vector_index(milvus_collection, "question_vec", index_params)
    # Create Index on PythonBooks
    index_params = {
        "metric_type": "COSINE",
        "index_type": "HNSW",
        "params": {"M": 16,  # int. 4~64, num_neighbors, higher values takes more memory.
                   "efConstruction": 32  # int. 8~512, num_candidate_nearest_neighbors
                   },
        "index_name": "PythonBooks_HNSW"
    }
    # Create an IVF_FLAT index for collection. Not used for now.
    index_params_ivf = {
        'metric_type': 'L2',
        'index_type': "IVF_FLAT",
        'params': {'nlist': 1536}
    }
    create_vector_index(milvus_collection_v2, "book_chunk_vec", index_params)
    print("Indexes: ", utility.list_indexes("PythonQA"),
          utility.list_indexes("PythonBooks")
          )
    disconnect_from_milvus(milvus_connection)
