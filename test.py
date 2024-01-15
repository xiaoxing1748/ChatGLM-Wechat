# import qianfan_api as qianfan
# import chatglm_api as chatglm
import faiss_vector_store as faiss_vector_store
import knowledge_chain as knowledge_chain
import embeddings
from config_loader import ConfigLoader as config


# 初始化向量存储
def get_vector_store():
    # 加载embedding
    embedding = embeddings.load()
    # 向量存储
    return faiss_vector_store.index(document_path, embedding)


# 搜寻文档
def get_docs(question):
    return faiss_vector_store.search(question, document_path, vector_store)


def format_docs(docs):
    # context = []
    # 遍历docs中的每个元素，提取page_content并添加到context
    # for doc in docs:
    #     context.append(doc[0].page_content)
    return "\n".join(doc[0].page_content for doc in docs)
    # print(context)


config = config()
apikey = config.get_qianfan_config("apikey")
secretkey = config.get_qianfan_config("secretkey")
serviceid = config.get_qianfan_config("serviceid")


# 文档路径
document_path = "./knowledge_base/本地知识库.csv"
# 向量存储
vector_store = ""
# vector_store = get_vector_store()

question = "学校地址是什么？"
question = "你好"

# docs = get_docs(question)
# print(format_docs(docs))
# exit()

# response = knowledge_chain.qa_chain_legacy(question, vector_store)
# response = knowledge_chain.qa_chain(question, vector_store)

response = knowledge_chain.qianfan_chain(
    apikey, secretkey, question, vector_store)
# response = knowledge_chain.qianfan_chain(
#     apikey, secretkey, question)

print(response)
