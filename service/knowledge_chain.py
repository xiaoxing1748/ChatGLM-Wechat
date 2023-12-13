# https://python.langchain.com/docs/integrations/llms/chatglm
from langchain.chains import LLMChain
from langchain.llms import ChatGLM
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
import vector_store


def get_knowledge_based_answer(context=None, question=None):
    answer = ""
    return answer


# Legacy mode
def llm_run(question=None, docs=None):

    knowledge = []
    # 遍历docs中的每个元素，提取page_content并添加到context
    for doc in docs:
        knowledge.append(doc[0].page_content)
    template = """基于以下【已知内容】的问答对，回答用户提出的【问题】，并遵循如下规则：
    1、每个问答对的问题以ask:开头，而回答以answer:开头。
    2、你的回答不应该以“根据已知内容”开头，请直接进行回答。
    3、如果无法从中得到答案，请说 "抱歉，我无法回答该问题"，此外不允许在答案中添加编造成分。

    【已知内容】:
    {knowledge}
    
    【问题】:
    {question}"""
    prompt = PromptTemplate(template=template, input_variables=[
                            "knowledge", "question"])

    endpoint_url = "http://127.0.0.1:8000"

    llm = ChatGLM(
        endpoint_url=endpoint_url,
        max_token=8000,
        history=[],
        top_p=0.9,
        model_kwargs={"sample_model_args": False},
    )

    llm_chain = LLMChain(prompt=prompt, llm=llm)
    answer = llm_chain.run(question=question, knowledge=knowledge)
    return answer


# LECL mode
def llm_run1(question=None):
    prompt = PromptTemplate.from_template(
        "{question}"
    )
    runnable = prompt | llm_run() | StrOutputParser()
    runnable.invoke({"question": question})
    # return runnable


if __name__ == '__main__':
    question = "你的已知内容有什么？"
    # question = ""
    docs = vector_store.search(question, "./document/news.txt")
    answer = llm_run(question=question, docs=docs)
    print(answer)
