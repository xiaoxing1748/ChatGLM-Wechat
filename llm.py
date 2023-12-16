# https://python.langchain.com/docs/integrations/llms/chatglm
from langchain.llms import ChatGLM


def chatglm(endpoint_url=None):
    """return llm\n
    实例化LLM模型"""
    if endpoint_url is None and endpoint_url != "":
        endpoint_url = "http://127.0.0.1:8000"
    llm = ChatGLM(
        endpoint_url=endpoint_url,
        max_token=8000,
        history=[],
        top_p=0.9,
        model_kwargs={"sample_model_args": False},
    )
    return llm
