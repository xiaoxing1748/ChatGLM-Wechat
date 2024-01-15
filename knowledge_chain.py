from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import QianfanChatEndpoint
import os
from llm import chatglm


# 加载prompt
with open("./prompt.txt", 'r', encoding='utf-8') as file:
    template = file.read()


# 文档格式化 索引完的文档格式与原始格式不一致因此不需要doc[0].page_content
def format_docs(docs):
    return "\n".join(doc.page_content for doc in docs)


# LCEL chain
def llm_chain(question):
    prompt = PromptTemplate(
        template="{question}", input_variables=["question"])
    model = chatglm()
    chain = (
        {"question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser())
    return chain.invoke(question)


# LCEL qianfan chain
def qianfan_chain(apikey, secretkey, question, model=None):
    os.environ["QIANFAN_AK"] = apikey
    os.environ["QIANFAN_SK"] = secretkey
    model = QianfanChatEndpoint(
        model=model if model else "ChatGLM2-6B-32K",
    )
    prompt = PromptTemplate(
        template="{question}", input_variables=["question"])
    output_parser = StrOutputParser()
    chain = (
        {"question": RunnablePassthrough()}
        | prompt
        | model
        | output_parser
    )
    return chain.invoke(question)


# LCEL QA chain
# https://python.langchain.com/docs/use_cases/question_answering/local_retrieval_qa
def qa_chain(question, vector_store):
    retriever = vector_store.as_retriever()
    prompt = PromptTemplate(template=template, input_variables=[
                            "context", "question"])
    output_parser = StrOutputParser()
    model = chatglm()
    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | model
        | output_parser
    )
    return chain.invoke(question)


# LCEL qianfan QA chain
# https://python.langchain.com/docs/integrations/chat/baidu_qianfan_endpoint
# https://python.langchain.com/docs/use_cases/question_answering/quickstart
def qianfan_qa_chain(apikey, secretkey, question, vector_store, model=None):
    os.environ["QIANFAN_AK"] = apikey
    os.environ["QIANFAN_SK"] = secretkey
    model = QianfanChatEndpoint(
        model=model if model else "ChatGLM2-6B-32K",
    )
    retriever = vector_store.as_retriever()
    prompt = PromptTemplate(template=template, input_variables=[
                            "context", "question"])
    output_parser = StrOutputParser()
    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | model
        | output_parser
    )
    return chain.invoke(question)
