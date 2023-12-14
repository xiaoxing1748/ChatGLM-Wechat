# https://python.langchain.com/docs/integrations/llms/chatglm
from langchain.chains import LLMChain
from langchain.llms import ChatGLM
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import QianfanChatEndpoint
import api.qianfan_api as qianfan_api
from config_loader import ConfigLoader
from langchain_core.language_models.chat_models import HumanMessage
import os


# Legacy LLM mode
def llm_run(question=None):
    template = """基于以下【已知内容】，请简洁并专业地回答用户提出的【问题】。如果无法从中得到答案，请说 "根据已知信息无法回答该问题"，此外不允许在答案中添加编造成分。【已知内容】:{context}【问题】:{question}"""
    prompt = PromptTemplate(template=template, input_variables=["question"])
    model = chatglm()
    llm_chain = LLMChain(prompt=prompt, llm=model)
    answer = llm_chain.run(question)
    return answer


# LECL LLM mode
# https://python.langchain.com/docs/expression_language/get_started#rag-search-example
def llm_chain(question=None, context=None, prompt=None):

    if prompt is None:
        # 两种prompt模板不同 前者具有角色配置
        # prompt = ChatPromptTemplate.from_template(
        #     "{question}"
        # )
        prompt = PromptTemplate.from_template(
            "{question}"
            # "基于以下【已知内容】的问答对，回答用户提出的【问题】，并遵循如下规则：\n1、每个问答对的问题以ask:开头，而回答以answer:开头。\n2、你的回答不应该以“根据已知内容”开头，请直接进行回答。\n3、如果无法从中得到答案，请说 '抱歉，我无法回答该问题'，此外不允许在答案中添加编造成分。\n【已知内容】:\n{context} \n【问题】:\n{question}"
        )
    output_parser = StrOutputParser()
    model = chatglm()
    chain = (
        {"question": RunnablePassthrough()}
        | prompt
        | model
        | output_parser
    )
    return chain.invoke(question)


# qianfan mode
# https://python.langchain.com/docs/integrations/chat/baidu_qianfan_endpoint
# langchain的问题暂时用不了 qianfan.errors.AccessTokenExpiredError
def qianfan_chain(accesskey, secretkey, content, model=None):
    os.environ["QIANFAN_AK"] = accesskey
    os.environ["QIANFAN_SK"] = secretkey
    chat = QianfanChatEndpoint(
        model=model,
    )
    # res = chat([HumanMessage(content=content)])
    res = chat([HumanMessage(content=content)])
    return res


# 单独实例化模型
def chatglm():
    """return llm\n
    实例化LLM模型"""
    endpoint_url = "http://127.0.0.1:8000"
    llm = ChatGLM(
        endpoint_url=endpoint_url,
        max_token=8000,
        history=[],
        top_p=0.9,
        model_kwargs={"sample_model_args": False},
    )
    return llm


def prompt_template(context=None, question=None):
    template = """基于以下【已知内容】的问答对，回答用户提出的【问题】，并遵循如下规则：
    1、每个问答对的问题以ask:开头，而回答以answer:开头。
    2、你的回答不应该以“根据已知内容”开头，请直接进行回答。
    3、如果无法从中得到答案，请说 "抱歉，我无法回答该问题"，此外不允许在答案中添加编造成分。

    【已知内容】:
    {context}
    
    【问题】:
    {question}"""
    prompt = PromptTemplate(template=template, input_variables=[
                            context, question])
    return prompt


if __name__ == '__main__':

    # question = "北京和上海两座城市有什么不同？"
    # llm_run(question)
    # print(llm_chain("你好"))
    # print(llm_chain("今年是哪一年？", "ask:今年是哪一年？ answer:今年是2025年"))
    config = ConfigLoader()
    sdkaccesskey = config.get_qianfan_config("sdkaccesskey")
    sdksecretkey = config.get_qianfan_config("sdksecretkey")
    model = config.get_qianfan_config("model")
    print(qianfan_chain(sdkaccesskey, sdksecretkey, "你好", model=model))
