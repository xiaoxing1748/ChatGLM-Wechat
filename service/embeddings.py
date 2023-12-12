from langchain.embeddings import HuggingFaceBgeEmbeddings
from text_splitter.chinese_text_splitter import ChineseTextSplitter
import document_loader
from langchain.vectorstores import FAISS
from langchain.schema import Document


def load(model_name=None):
    # 使用CPU
    # model_kwargs = {'device': 'cpu'}

    # 使用GPU
    model_kwargs = {'device': 'cuda'}
    if model_name is None:
        model_name = r"F:\ChatGLM\embedding\bge-large-zh-v1.5"
    encode_kwargs = {'normalize_embeddings': True}
    model = HuggingFaceBgeEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs,
    )
    return model


if __name__ == '__main__':
    embeddings = load()
    text = document_loader.load_and_split_unstructured("./document/test.txt")
    print(text)
    vector_store = FAISS.from_documents(text, embeddings)
    query = "智能手机"
    docs = vector_store.similarity_search(query)
    # 返回索引第一条
    print(docs[0].page_content)
