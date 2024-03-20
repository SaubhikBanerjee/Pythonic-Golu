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
