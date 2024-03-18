# I am running my LLM locally on CPU - Data Privacy!!
# Good read: https://towardsdatascience.com/running-llama-2-on-cpu-inference-for-document-q-a-3d636037a3d8
#          : https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/tree/main

from langchain_community.llms import CTransformers
from libs.read_config import ReadConfig

# Local CTransformers wrapper for Llama-2-7B-Chat
my_config = ReadConfig("config/config.ini")
local_llm = CTransformers(model=my_config.llm_path,
                          model_type='llama',  # Model type Llama
                          config={'max_new_tokens': int(my_config.max_new_tokens),
                                  'temperature': float(my_config.temperature),
                                  'context_length': int(my_config.context_length)})

if __name__ == '__main__':
    print(type(local_llm))
