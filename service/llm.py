# https://python.langchain.com/docs/integrations/llms/chatglm
from langchain.chains import LLMChain
from langchain.llms import ChatGLM
from langchain.prompts import PromptTemplate
import vector_store


def get_knowledge_based_answer(context=None, question=None):
    # docs=vector_store.load_and_search(question, "./document/news.txt")

    template = """基于以下【已知内容】，请简洁并专业地回答用户提出的【问题】。
                                            如果无法从中得到答案，请说 "根据已知信息无法回答该问题"，此外不允许在答案中添加编造成分。
                                            【已知内容】:
                                            {context}
                                            【问题】:
                                            {question}"""
    template1 = """请输出你接收到的【已知内容】,【已知内容】如下:{context}"""
    prompt = PromptTemplate(template=template, input_variables=[
                            "context", "question"])
    endpoint_url = "http://localhost:8000"
    llm = ChatGLM(
        endpoint_url=endpoint_url,
        max_token=8000,
        history=[],
        top_p=0.9,
        model_kwargs={"sample_model_args": False},
    )

    # llm.with_history = True
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    # question = "北京和上海两座城市有什么不同？"
    print(llm_chain.run({'context': context, 'question': question}))
    # ChatGLM payload: {'prompt': '北京和上海两座城市有什么不同？', 'temperature': 0.1, 'history': [['我将从美国到中国来旅游，出行前希望了解中国的城市', '欢迎问我任何问题。']], 'max_length': 80000, 'top_p': 0.9, 'sample_model_args': False}


if __name__ == '__main__':
    question = "今天星期几？"
    question = ""
    context = vector_store.search(question, "./document/news.txt")
    get_knowledge_based_answer(context=context, question=question)
