# Good Read: https://github.com/christy/ZillizDemos/blob/main/milvus_onboarding/hello_world_milvus.ipynb

from sentence_transformers import SentenceTransformer
# Make it libs.read_config after unit testing.
from libs.read_config import ReadConfig
from pymilvus import (Collection, connections, utility)
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Milvus


def milvus_vector_search_book(user_query):
    my_config = ReadConfig("config/config.ini")
    model_name = my_config.SentenceTransformer_model
    model = SentenceTransformer(model_name)
    # Return top k results with HNSW index.
    top_k = int(my_config.search_top_k)
    search_parameters = {
        "metric_type": "COSINE",
        "offset": 0,
        "ignore_growing": False,
        "params": {"ef": 32}
    }
    # Embed the query using same embedding model used to create the Milvus collection
    user_query_embedding = model.encode(user_query)
    connections.connect("default",
                        host=my_config.host,
                        port=int(my_config.port),
                        user=my_config.user,
                        password=None,
                        show_startup_banner=True
                        )
    print("Connected to Milvus!")
    # Check if the server is ready.
    print("Database Version: ", utility.get_server_version())
    # Loading collection
    milvus_collection = Collection("PythonBooks")
    # Before conducting a search based on a query, you need to load the data into memory.
    milvus_collection.load()
    results = milvus_collection.search(
        data=[user_query_embedding],
        anns_field="book_chunk_vec",
        param=search_parameters,
        output_fields=["book_name", "book_author", "book_chunk"],
        limit=top_k
    )
    milvus_collection.release()
    connections.disconnect("default")
    return results


def milvus_vector_search_langchain_book(user_query):
    my_config = ReadConfig("config/config.ini")
    top_k = int(my_config.search_top_k)
    search_parameters = {
        "metric_type": "COSINE",
        "offset": 0,
        "ignore_growing": False,
        "params": {"ef": 32}
    }
    model_name = my_config.SentenceTransformer_model
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    connection_args = {"host": my_config.host,
                       "port": int(my_config.port),
                       "user": my_config.user,
                       "password": None
                       }
    # Get existing collection from Milvus with changing index parameters
    vector_db: Milvus = Milvus(
        embedding_function=embeddings,
        collection_name="PythonBooks",
        search_params=search_parameters,
        connection_args=connection_args,
        text_field="book_chunk",
        vector_field="book_chunk_vec",
        consistency_level="Session"
    )

    # Tested similarity search using LangChain.
    # docs = vector_db.similarity_search(query=user_query, k=top_k)
    docs = vector_db.similarity_search_with_score(query=user_query, k=top_k)
    return docs


if __name__ == '__main__':
    my_query = input("What is your query:")
    search_results = milvus_vector_search_book(my_query)
    for hits_i, hits in enumerate(search_results):
        print('Results:')
        print("=============")
        for rank, hit in enumerate(hits):
            print("\033[92m Rank: \033[0;0m", rank+1)
            print("\033[92m========\033[0;0m")
            print("\033[92m Chunk: \033[0;0m", hit.entity.get('book_chunk'))
            print('\033[38;5;208mScore: ====>\033[0;0m', hit.distance)
            print("*"*40)
