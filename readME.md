### ![milvus_icon.png](images%2Fmilvus_icon.png) ![python_icon.png](images%2Fpython_icon.png)
# Pythonic Golu: A Retrieval Augmented Generation (RAG) application using Milvus and Python.
### Who, When, Why?
👨🏾‍💻 Author: Saubhik Banerjee <br />
📅 Version: 1.0 March 2024<br />
📜 License: This project is licensed under the MIT license. Please feel free to use it, 
    just don't do bad things with it.

## Aim of Pythonic Golu
The Pythonic Golu has the aim to answer any Python question on the earth! and specifically
all the questions asked in PCEP, PCAP and LinkedIn Python tests.<br />
I will try to host it with Streamlit cloud with a persistence Milvus instance, so that people
can leverage my huge Python database of question and answers.<br />
At present, you can use it in your local Milvus with your own dataset. Just clone this repo and 
get started!  ***Pythonic Golu is completely on open source, so no extra cost!!***
### How to get/run Milvus?
Well, I am using a docker compose file, which is part of the repository. You can use that too
and necessary command to get start with that image is also given.
### What is RAG and Why?
When we ask a question to LLM, LLM can answer based on what it is trained on, but what if
we have our own data / private knowledge base? for example, you have your own Python question 
answer knowledgebase based on various certification exams.
This data is not public and LLM is not trained on this. Also, if you need very current data
for example: question based on 5th India England Test Match 2024. In those cases RAG (**R**etrieval-**A**ugmented **G**eneration)
comes for your rescue.
Using RAG a context information can be produced to LLM from our own unstructured data.
#### RAG Vs Fine Tuning
Why not fine-tuning a LLM? Well tuning a LLM is time and effort consuming. It need specialized expertise.
On top of that training LLM has a huge cost. You need to constantly train your LLM as your data
will probably evolve with respect to time (e.g. new Python questions in various tests).
So, in that case RAG gives an cost-effective yet optimized solution.
### General RAG Architecture
What is general RAG architecture? This diagram is taken from **IBM** architectural document which 
neatly describes the general RAG architecture.
![general_rag.png](images%2Fgeneral_rag.png)
### Architecture of Pythonic GOLU
Technically I am using Milvus v2.3.7 and Python 3.11.3. The over all architecture looks like:
![golu_architecture.png](images%2Fgolu_architecture.png)
### The files in this repository
#### [milvus_test.py](milvus_test.py): 
This is a test file, it has been created during my initial interaction with Milvus. This is not 
actually part of "Pythonic Golu", but I kept it assuming it might be useful for some of you who are starting 
fresh in Milvus!.
#### [create_collection_and_index.py](create_collection_and_index.py):
This file is used for creating the two main Milvus collections namely 1. PythonBooks and 2. PythonQA
This also creats the indexes associated with these collections.
This program internally using the Python module [milvus_utils.py](libs%2Fmilvus_utils.py)
which does the actual job. All the modules written for this project resides in libs directory.
#### [load_python_books.py](load_python_books.py):
This is the main file used to load various Python Books into Milvus! All the actual work is done by the
Python module called [load_books.py](libs%2Fload_books.py)
#### [golu.py](golu.py):
This file is currently under development. I have a plan to deploy Pythonic Golu in Streamlit 
cloud along with some persistence Milvus instance. To run this use ***`streamlit run .\golu.py`***
This is locally functional and can produce output.
#### [flush_all_milvus_collection.py](libs%2Fflush_all_milvus_collection.py):
This is a stand-alone file used to flush and compacting Milvus collection. There is a problem with flush
in earlier version of Milvus. https://github.com/milvus-io/milvus/discussions/31195
#### [semantic_search.py](libs%2Fsemantic_search.py):
This is the library used to do a semantic search on Milvus with your question!.
#### [run_semantic_search.py](run_semantic_search.py):
Run some native semantic search using native Pymilvus. Internally it is using [semantic_search.py](libs%2Fsemantic_search.py)
#### [run_semantic_search_langchain.py](run_semantic_search_langchain.py):
Run semantic search using Langchain. This is also internally using [semantic_search.py](libs%2Fsemantic_search.py)
#### [ask_questions_v1.py](ask_questions_v1.py):
Join all the pieces together and get a response from local LLM using LangChain RetrievalQA.

### Why Pythonic Golu is slow?
Well, I have observed this as one of the problem with Golu. I am running this in my laptop
which doesn't have any GPU. I am only relying on CPU.
If you have GPU power, then definitely that will be faster.
# Startup 🚀
1. Clone this repo `git clone https://github.com/SaubhikBanerjee/Pythonic-Golu`
2. Go into the directory `cd Pythonic-Golu`
3. Setup your Milvus database and update config.ini accordingly.
4. Run  [create_collection_and_index.py](create_collection_and_index.py) to create Milvus collections & indexes.
5. Run  [load_python_books.py](load_python_books.py) to load some data from your documents.
6. Now try some semantic search! [run_semantic_search.py](run_semantic_search.py) and [run_semantic_search_langchain.py](run_semantic_search_langchain.py)
7. Next try asking some questions![ask_questions_v1.py](ask_questions_v1.py)
8. Lastly try the web interface using Streamlit!! ***`streamlit run .\golu.py`***

#### AWS profile creation using AWS CLI
Download and install AWS CLI from https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html based on our operating system.
Use `aws configure --profile your_profile_name` and use this profile name in your configuration file. For more information please refer to AWS user guide.

#### How to download a local LLM?
https://towardsdatascience.com/running-llama-2-on-cpu-inference-for-document-q-a-3d636037a3d8
https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/tree/main


