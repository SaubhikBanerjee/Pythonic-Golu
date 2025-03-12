# Good reads : https://arxiv.org/pdf/2312.16171.pdf
#            : https://medium.com/the-modern-scientist/best-prompt-techniques-for-best-llm-responses-24d2ff4f6bca
#            : https://towardsdatascience.com/how-i-won-singapores-gpt-4-prompt-engineering-competition-34c195a93d41


qa_template = """Use the following pieces of context to answer the user's question.
If you don't know the answer based on the context only, just say that you don't know, don't try to make up an answer.
Give the reference document or link if available. Give explanation if available. Think step by step.

Context: {context}
Question: {question}

Only return the helpful answer then reference / explanation each in new line below and nothing else.
If you don't know the answer based on the context say you don't know.
Helpful answer:

"""
qa_template_zephyr = """
<|system|>
Using the information contained in the context, 
give a concise answer to the question, If the answer is contained in the context, also report the reference URL.
If the answer cannot be deduced from the context say I don't know.
</s>
<|user|>
Context: {context}
Question: {question}
Remember only return AI answer
</s>
<|assistant|>
"""

qa_template_phi = """
<|system|>
Using the information contained in the context, 
give a concise answer to the question, If the answer is contained in the context, also report the reference URL.
If the answer cannot be deduced from the context say I don't know.
<|end|>
<|user|>
Context: {context}
Question is below. Remember only return AI answer
Question: {question}
<|end|>
<|assistant|>
"""

query_expansion = """You are an AI language model assistant. Your task is to generate {to_expand_to_n}
    different versions of the given user question to retrieve relevant documents from a vector
    database. By generating multiple perspectives on the user question, your goal is to help
    the user overcome some of the limitations of the distance-based similarity search.
    Provide these alternative questions separated by '{separator}'.
    Original question: {question}"""

self_query = """You are an AI language model assistant. Your task is to extract information from a user question.
    The required information that needs to be extracted is the keywords. 
    Your response should consists of only the extracted keywords, nothing else.
    User question: {question}"""