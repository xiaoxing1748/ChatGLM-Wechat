# https://python.langchain.com/docs/integrations/vectorstores/faiss
import document_loader
from langchain.vectorstores import FAISS
import embeddings
from config_reader import config_reader


# 加载embedding
embedding_path = config_reader.get_embedding_path()
embedding = embeddings.load(embedding_path)


# FAISS向量存储
def index(document_path):
    # 加载并分割文档
    text = document_loader.load_and_split_unstructured(document_path)
    # 输出分割完的文档
    print(text)
    # 构建向量存储
    vector_store = FAISS.from_documents(text, embedding)
    # 保存索引
    vector_store.save_local("faiss_index")
    return vector_store


# 查询
def search(query, document_path):
    vector_store = index(document_path)
    # 查询向量
    # docs = vector_store.similarity_search(query)
    # 查询带分数的向量
    docs = vector_store.similarity_search_with_score(query)
    return docs


# 加载索引并搜索
def load_and_search(query):
    vector_store = FAISS.load_local("faiss_index", embedding)
    docs = vector_store.similarity_search_with_score(query)
    return docs


if __name__ == '__main__':
    docs = search("摘要", "./document/news.txt")
    # docs = load_and_search("星期四")
    for doc in docs:
        print(doc)
    print("--------------------")
    context = []
    # 遍历docs中的每个元素，提取page_content并添加到context
    for doc in docs:
        context.append(doc[0].page_content)
    print(context)
