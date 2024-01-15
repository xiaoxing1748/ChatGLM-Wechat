# https://python.langchain.com/docs/integrations/vectorstores/faiss
import document_loader
from langchain_community.vectorstores import FAISS
import embeddings


# FAISS向量存储
def index(document_path, embedding=None, log=None):
    """return vector_store"""
    # 加载文档
    text = document_loader.load(document_path)
    # 输出分割完的文档
    if log is not None:
        print(text)
    print("文档加载完成")
    # 构建向量存储
    if embedding is None:
        embedding = embeddings.load()
    vector_store = FAISS.from_documents(text, embedding)
    # 保存索引
    vector_store.save_local("faiss_index")
    print("索引完成")
    return vector_store


# 加载索引
def load(embedding=None):
    """return vector_store"""
    if embedding is None:
        embedding = embeddings.load()
    return FAISS.load_local("faiss_index", embedding)


# 查询
def search(query, document_path, vector_store=None):
    """return docs"""
    if vector_store is None:
        vector_store = index(document_path)
    # 查询向量
    # docs = vector_store.similarity_search(query)
    # 查询带分数的向量
    docs = vector_store.similarity_search_with_score(query)
    print("检索完成")
    return docs


# 加载索引并搜索
def load_and_search(query):
    """return docs"""
    docs = load().similarity_search_with_score(query)
    return docs
