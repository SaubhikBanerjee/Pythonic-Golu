"""
This will be used to load Python books into the collection PythonBooks.
It takes filename (with path), book name and author name as command line argument.
"""
from libs import load_python_book_into_milvus
import sys


if __name__ == '__main__':
    help_text = """ 
                You have to pass at least one parameter. Three parameters can be passed.
                They are filename with path, book name and author. 
                If you don't know the book name and author please pass it as "Unknown"
                Example: python load_python_books.py "C:\\xyz.docx" "My Book" "My Author" 
                         python load_python_books.py "C:\\xyz.docx" "Unknown" "Unknown"
                """
    # At least one parameter is required.
    if len(sys.argv[1:]) == 0:
        print(help_text)
        sys.exit(0)

    # Exactly three parameters expected.
    if len(sys.argv[1:]) != 3:
        print(help_text)
        sys.exit(0)

    if len(sys.argv[1:]) == 3:
        print(sys.argv[1])
        print(sys.argv[2])
        print(sys.argv[3])
    load_python_book_into_milvus(sys.argv[1],
                                 sys.argv[2],
                                 sys.argv[3]
                                 )
