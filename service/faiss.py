# https://python.langchain.com/docs/integrations/vectorstores/faiss
import document_loader
from langchain.vectorstores import FAISS
import embeddings
from config_reader import config_reader


def search(query, document_path):
    embedding_path = config_reader.get_embedding_path()
    # 加载embedding
    embedding = embeddings.load(embedding_path)
    # 加载并分割文档
    text = document_loader.load_and_split_unstructured(document_path)
    print(text)
    # 构建向量存储
    vector_store = FAISS.from_documents(text, embedding)
    # 查询向量
    # docs = vector_store.similarity_search(query)
    # 查询带分数的向量
    docs = vector_store.similarity_search_with_score(query)
    # 返回索引第一条的page_content
    print(docs[0].page_content)
    # print("\n")
    # # 或者遍历输出
    # for doc in docs:
    #     print(doc)


if __name__ == '__main__':
    search("丁真问啥牌子的啤酒味道好", "./document/news.txt")
