# https://python.langchain.com/docs/integrations/llms/chatglm
from langchain.chains import LLMChain
from langchain.llms import ChatGLM
from langchain.prompts import PromptTemplate
import vector_store


question = "丁真问啥牌子的啤酒味道好"


def get_knowledge_based_answer(question):
    docs = vector_store.search(question, "./document/news.txt")
    # docs=vector_store.load_and_search(question, "./document/news.txt")

    template = """基于以下【已知内容】，请简洁并专业地回答用户提出的【问题】。
                                            如果无法从中得到答案，请说 "根据已知信息无法回答该问题"，此外不允许在答案中添加编造成分。
                                            【已知内容】:
                                            {context}
                                            【问题】:
                                            {question}"""
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

    print(llm_chain.run(question))


if __name__ == '__main__':
    get_knowledge_based_answer(question)
