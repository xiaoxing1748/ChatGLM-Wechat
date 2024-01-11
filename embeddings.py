# https://python.langchain.com/docs/integrations/text_embedding
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
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
