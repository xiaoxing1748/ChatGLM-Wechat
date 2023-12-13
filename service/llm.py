# https://python.langchain.com/docs/integrations/llms/chatglm
from langchain.chains import LLMChain
from langchain.llms import ChatGLM
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate


# Legacy mode
def llm_run(question=None):
    template = """基于以下【已知内容】，请简洁并专业地回答用户提出的【问题】。如果无法从中得到答案，请说 "根据已知信息无法回答该问题"，此外不允许在答案中添加编造成分。【已知内容】:{context}【问题】:{question}"""
    prompt = PromptTemplate(template=template, input_variables=["question"])

    # default endpoint_url for a local deployed ChatGLM api server
    endpoint_url = "http://127.0.0.1:8000"

    # direct access endpoint in a proxied environment
    # os.environ['NO_PROXY'] = '127.0.0.1'

    llm = ChatGLM(
        endpoint_url=endpoint_url,
        max_token=8000,
        history=[],
        top_p=0.9,
        model_kwargs={"sample_model_args": False},
    )
    # turn on with_history only when you want the LLM object to keep track of the conversation history
    # and send the accumulated context to the backend model api, which make it stateful. By default it is stateless.
    # llm.with_history = True

    llm_chain = LLMChain(prompt=prompt, llm=llm)
    answer = llm_chain.run(question)
    return answer


# LECL mode
def llm_chain(question=None, prompt=None):

    if prompt is None:
        # 两种prompt模板不同 前者具有角色配置
        # prompt = ChatPromptTemplate.from_template(
        #     "{question}"
        # )
        prompt = PromptTemplate.from_template(
            "{question}"
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


# 单独实例化模型
def chatglm():
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
    print(llm_chain("你好"))
