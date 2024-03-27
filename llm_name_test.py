from langchain_community.llms import CTransformers
from langchain_community.llms import HuggingFaceHub
from libs.read_config import ReadConfig
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


my_config = ReadConfig("config/config.ini")
prompt = ChatPromptTemplate.from_template("You are a expert chat assistant. Answer the following question {question}")
# Local CTransformers wrapper for Llama-2-7B-Chat
local_llm = CTransformers(model=r"C:\Saubhik\Project Automation\hybrid_search\lama2\llama-2-7b-chat.Q8_0.gguf",
                          model_type='llama',  # Model type Llama
                          config={'max_new_tokens': 512,
                                  'temperature': 0.001,
                                  'context_length': 1024})

# zephyr-7b-beta Using HuggingFaceHub
# Use your own huggingfacehub_api_token !!
zephyr_llm = HuggingFaceHub(repo_id="HuggingFaceH4/zephyr-7b-beta",
                            model_kwargs={"temperature": 0.001,
                                          "max_new_tokens": 512,
                                          "repetition_penalty": 1.1,
                                          "max_length": 64,
                                          "top_p": 0.9,
                                          "return_full_text": False
                                          },
                            huggingfacehub_api_token=my_config.hf_api_token
                            )

# Testing with OpenAI -- remember this is paid.
# Use your own OpenAI API key!!
openai_llm = ChatOpenAI(model_name="gpt-3.5-turbo",
                        temperature=0.001,
                        openai_api_key=my_config.openai_api_key
                        )

if __name__ == '__main__':
    chain = prompt | local_llm | StrOutputParser()
    output = chain.invoke({"question": "What is your official name as LLM?"})
    print('\n\033[92m Local llama-2-7b-chat.Q8_0.gguf: \033[0;0m')
    print(output)
    chain = prompt | zephyr_llm | StrOutputParser()
    output = chain.invoke({"question": "What is your official name as LLM?"})
    print('\n\033[92m HuggingFaceH4/zephyr-7b-beta: \033[0;0m')
    print(output)
    chain = prompt | openai_llm | StrOutputParser()
    output = chain.invoke({"question": "What is your official name as LLM?"})
    print('\n\033[92m gpt-3.5-turbo: \033[0;0m')
    print(output)

