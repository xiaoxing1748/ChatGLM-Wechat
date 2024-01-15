from config_loader import ConfigLoader as config
# import qianfan_api as qianfan
# import chatglm_api as chatglm
import faiss_vector_store as faiss_vector_store
import knowledge_chain as knowledge_chain
import embeddings


config = config()


# 初始化向量存储
def get_vector_store():
    # 加载embedding
    embedding = embeddings.load()
    # 向量存储
    return faiss_vector_store.index(document_path, embedding)


# 搜寻文档
def get_docs(question):
    return faiss_vector_store.search(question, document_path, vector_store)


# 文档路径
document_path = "./knowledge_base/本地知识库.csv"
# 向量存储
vector_store = get_vector_store()
question = "学校地址是什么？"
# print(get_docs(question))
# response = knowledge_chain.qa_chain_legacy(question, vector_store)
response = knowledge_chain.llm_chain(question, vector_store)
print(response)
