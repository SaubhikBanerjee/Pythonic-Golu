"""
This file is used to do the semantic search on Milvus. This files calls the function
milvus_vector_search_book which is on the libs/semantic_search.py.
The semantic_search module is actually doing the heavy lifting.
"""
from libs import milvus_vector_search_book


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
