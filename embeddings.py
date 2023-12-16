# https://python.langchain.com/docs/integrations/text_embedding
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings
import document_loader
from langchain.vectorstores import FAISS
from config_loader import ConfigLoader


# 加载embedding
def load(model_name=None):
    # model_kwargs = {'device': 'cpu'}
    model_kwargs = {'device': 'cuda'}
    encode_kwargs = {'normalize_embeddings': True}

    if model_name is None:
        model_name = ConfigLoader().get_embedding_path()

    # 匹配BGE embeddings 其他懒得写了照抄文档就行
    # https://python.langchain.com/docs/integrations/text_embedding
    if 'bge' in model_name and 'v1.5' in model_name:
        model = HuggingFaceBgeEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs,
        )
    else:
        model = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs,
        )
    return model


if __name__ == '__main__':
    # 加载embedding
    embedding = load()
    # 加载并分割文档
    text = document_loader.load_and_split_unstructured("./document/news.txt")
    print(text)
    print("\n")
    # 构建向量存储
    vector_store = FAISS.from_documents(text, embedding)
    query = "丁真问啥牌子的啤酒味道好"
    # 查询向量
    # docs = vector_store.similarity_search(query)
    # 查询带分数的向量
    # docs = vector_store.similarity_search_with_score(query)
    # 返回索引第一条的page_content
    # print(docs[0].page_content)
    # print("\n")
    # 或者遍历输出
    # for doc in docs:
    #     print(doc)
    # print("")
