"""
This module will load the PythonBooks collection. Currently, it is using a simple
chunking technique using Langchain RecursiveCharacterTextSplitter with Unstructured.
RAG is as good as your data, So more advanced chunking techniques will be provided
in latter releases.
"""
import sys
import uuid
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from unstructured.cleaners.core import (clean_extra_whitespace,
                                        replace_unicode_quotes,
                                        group_broken_paragraphs,
                                        clean_non_ascii_chars
                                        )
import os
from transformers import AutoTokenizer
from sentence_transformers import SentenceTransformer
# Make it libs.read_config after unit testing.
from libs.read_config import ReadConfig
from unstructured.documents.elements import Text
import re
from pymilvus import (Collection, connections, utility)


def load_file(filename):
    document_maps = {
        ".md": UnstructuredMarkdownLoader,
        ".pdf": UnstructuredPDFLoader,
        ".xls": UnstructuredExcelLoader,
        ".xlsx": UnstructuredExcelLoader,
        ".docx": UnstructuredWordDocumentLoader,
        ".doc": UnstructuredWordDocumentLoader,
    }
    file_extension = os.path.splitext(filename)[1].lower()
    if file_extension in document_maps:
        loader_class = document_maps.get(file_extension)
        loader = loader_class(filename)
        file_data = (loader.load()[0])
        return file_data
    else:
        # Am I too rigid here?
        print("Unsupported extension!")
        sys.exit(0)


def split_in_chunks_v2(my_document):
    HF_EOS_TOKEN_LENGTH = 1
    my_config = ReadConfig("config/config.ini")
    model_name = my_config.SentenceTransformer_model
    model = SentenceTransformer(model_name)
    # print("Model max sequence length:", model.max_seq_length)
    text_splitter = (
        RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
            tokenizer=AutoTokenizer.from_pretrained(model_name),
            chunk_size=model.max_seq_length - HF_EOS_TOKEN_LENGTH,
            chunk_overlap=int((model.max_seq_length - HF_EOS_TOKEN_LENGTH) / 5)
        ))
    texts = text_splitter.split_documents(my_document)
    return texts


def load_python_book(filename):
    book_data = load_file(filename)
    # Pay detail attention to those tiny []!! will save you lots of time.
    # [book_data] -- split_documents expects a list of Documents!!
    text_chunks = split_in_chunks_v2([book_data])
    return text_chunks


def clean_chunk_data(chunk_data):
    element = Text(chunk_data.page_content)
    element = str(element)
    element = replace_unicode_quotes(element)
    element = element.replace("`", "")
    element = clean_extra_whitespace(element)
    para_split_re = re.compile(r"(\s*\n\s*){3}")
    element = group_broken_paragraphs(element, paragraph_split=para_split_re)
    element = clean_extra_whitespace(element)
    element = clean_non_ascii_chars(element)
    return element


def load_python_book_into_milvus(filename, book_name=None, book_author=None):
    try:
        my_config = ReadConfig("config/config.ini")
        # Connecting to my local Milvus in docker image.
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

        model_name = my_config.SentenceTransformer_model
        model = SentenceTransformer(model_name)
        book_chunks = load_python_book(filename)
        v_book_name = book_name
        v_book_author = book_author
        for chunk in book_chunks:
            book_chunk = clean_chunk_data(chunk)
            book_chunk_vec = model.encode(book_chunk)
            book_chunk_id = str(uuid.uuid4())
            # Insertion will be improved later with batch insert
            row_insert = [[book_chunk_id],
                          [v_book_name],
                          [v_book_author],
                          [book_chunk],
                          [book_chunk_vec]
                          ]
            insert_result = milvus_collection.insert(row_insert)
            print(insert_result)
        milvus_collection.flush()
        # Releasing the collection
        milvus_collection.release()
        connections.disconnect("default")

    except Exception as e:
        print("Problem in loading data!")
        print(e)
        sys.exit(0)
    finally:
        connections.disconnect("default")


if __name__ == '__main__':
    load_python_book_into_milvus(r"C:\Saubhik\Milvus\data\Python_LinkedIn_Question.docx",
                                 "Python_LinkedIn_Question",
                                 "Unknown"
                                 )
