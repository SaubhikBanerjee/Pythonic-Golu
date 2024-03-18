"""
This file is used to do the semantic search on Milvus using LangChain.
This files calls the function milvus_vector_search_langchain_book which is on the libs/semantic_search.py.
The semantic_search module is actually doing the heavy lifting.
"""
from libs import milvus_vector_search_langchain_book


if __name__ == '__main__':
    my_query = input("What is your query:")
    search_results = milvus_vector_search_langchain_book(my_query)
    print('Results:')
    print("=============")
    for rank, hits in enumerate(search_results):
        print("\033[92m Rank: \033[0;0m", rank+1)
        print("\033[92m========\033[0;0m")
        print("\033[92m Chunk: \033[0;0m", hits[0].page_content)
        print('\033[38;5;208mScore: ====>\033[0;0m', hits[1])
        print("*"*40)
