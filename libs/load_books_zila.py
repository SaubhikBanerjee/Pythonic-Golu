"""
This module will load the PythonBooks collection. Currently, it is using a simple
chunking technique using Langchain RecursiveCharacterTextSplitter with Unstructured.
RAG is as good as your data, So more advanced chunking techniques will be provided
in latter releases.
This particular file is used in Streamlit cloud.
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
from unstructured.documents.elements import Text
import re
from pymilvus import (Collection, connections, utility)
import streamlit as st
from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings


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
        print("Only .md, .pdf, .xls, .xlsx, .doc adn .docx is supported.")
        sys.exit(0)


def split_in_chunks_v2(my_document):
    print("Inside split_in_chunks_v2..")
    HF_EOS_TOKEN_LENGTH = 1
    model_name = st.secrets.LLM.SentenceTransformer_model
    model = SentenceTransformer(model_name)
    print("Model max sequence length:", model.max_seq_length)
    text_splitter = (
        RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
            tokenizer=AutoTokenizer.from_pretrained(model_name),
            chunk_size=model.max_seq_length - HF_EOS_TOKEN_LENGTH,
            chunk_overlap=int((model.max_seq_length - HF_EOS_TOKEN_LENGTH) / 5)
        ))
    texts = text_splitter.split_documents(my_document)
    return texts


def split_in_chunks_semantic(my_document):
    print("Inside split_in_chunks_semantic..")
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}
    model_name = st.secrets.LLM.SentenceTransformer_model
    model = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs,
    )
    semantic_chunker = SemanticChunker(model, breakpoint_threshold_type="percentile")
    semantic_chunks = semantic_chunker.create_documents([d.page_content for d in my_document])
    return semantic_chunks


def load_python_book(filename):
    print("Inside load_python_book..")
    book_data = load_file(filename)
    # Pay detail attention to those tiny []!! will save you lots of time.
    # [book_data] -- split_documents expects a list of Documents!!
    text_chunks = split_in_chunks_v2([book_data])
    print("Completed load_python_book..")
    return text_chunks


def load_python_book_semantic(filename):
    print("Inside load_python_book_semantic..")
    book_data = load_file(filename)
    # Pay detail attention to those tiny []!! will save you lots of time.
    # [book_data] -- split_documents expects a list of Documents!!
    text_chunks = split_in_chunks_semantic([book_data])
    print("Completed load_python_book_semantic..")
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
        # Connecting to my local Milvus in docker image.
        connections.connect("default",
                            uri=st.secrets.MILVUS.public_end_point,
                            token=st.secrets.MILVUS.zila_api_key
                            )
        print("Connected to Milvus!")
        # Check if the server is ready.
        print("Database Version: ", utility.get_server_version())
        # Loading collection
        milvus_collection = Collection("PythonBooks")
        print("Collection loaded...")

        model_name = st.secrets.LLM.SentenceTransformer_model
        model = SentenceTransformer(model_name)
        print("SentenceTransformer...")
        book_chunks = load_python_book(filename)
        print("Total chunks:", len(book_chunks))
        v_book_name = book_name
        v_book_author = book_author
        for chunk in book_chunks:
            book_chunk = clean_chunk_data(chunk)
            print("Cleaned the chunks..")
            book_chunk_vec = model.encode(book_chunk, normalize_embeddings=True)
            book_chunk_id = str(uuid.uuid4())
            # Insertion will be improved later with batch insert
            row_insert = [[book_chunk_id],
                          [v_book_name],
                          [v_book_author],
                          [book_chunk],
                          [book_chunk_vec]
                          ]
            print("Trying to insert...")
            insert_result = milvus_collection.insert(row_insert)
            print(insert_result)
        milvus_collection.flush()
        # Releasing the collection
        milvus_collection.release()
        connections.disconnect("default")

    except Exception as e:
        st.write("Problem in loading data!")
        st.write(e)
        sys.exit(0)
    finally:
        connections.disconnect("default")


def load_python_book_semantic_into_milvus(filename, book_name=None, book_author=None):
    try:
        # Connecting to my local Milvus in docker image.
        connections.connect("default",
                            uri=st.secrets.MILVUS.public_end_point,
                            token=st.secrets.MILVUS.zila_api_key
                            )
        print("Connected to Milvus!")
        # Check if the server is ready.
        print("Database Version: ", utility.get_server_version())
        # Loading collection
        milvus_collection = Collection("PythonBooks")
        print("Collection loaded...")

        model_name = st.secrets.LLM.SentenceTransformer_model
        model = SentenceTransformer(model_name)
        print("SentenceTransformer...")
        book_chunks = load_python_book_semantic(filename)
        print("Total chunks:", len(book_chunks))
        v_book_name = book_name
        v_book_author = book_author
        for chunk in book_chunks:
            book_chunk = clean_chunk_data(chunk)
            print("Cleaned the chunks..")
            book_chunk_vec = model.encode(book_chunk, normalize_embeddings=True)
            book_chunk_id = str(uuid.uuid4())
            # Insertion will be improved later with batch insert
            row_insert = [[book_chunk_id],
                          [v_book_name],
                          [v_book_author],
                          [book_chunk],
                          [book_chunk_vec]
                          ]
            print("Trying to insert...")
            insert_result = milvus_collection.insert(row_insert)
            print(insert_result)
        milvus_collection.flush()
        # Releasing the collection
        milvus_collection.release()
        connections.disconnect("default")

    except Exception as e:
        st.write("Problem in loading data!")
        st.write(e)
        sys.exit(0)
    finally:
        connections.disconnect("default")


if __name__ == '__main__':
    load_python_book_into_milvus(r"C:\Saubhik\Python\Books\Python Tricks The Book.pdf",
                                 "Python Tricks: The Book",
                                 "Dan Bader"
                                 )
    load_python_book_semantic_into_milvus(r"C:\Saubhik\Python\Books\Python Tricks The Book.pdf",
                                 "Python Tricks: The Book",
                                 "Dan Bader"
                                 )
