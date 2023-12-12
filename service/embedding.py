from langchain.embeddings import HuggingFaceBgeEmbeddings
from text_splitter.chinese_text_splitter import ChineseTextSplitter
import document_loader


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
    embedding = load()
    print(len(embedding.embed_query("文章标题")))
    text = document_loader.load("./document/test.txt")
    splitter = ChineseTextSplitter()
    splited_text = splitter.split_text(text[0].page_content)
    print(splited_text)
