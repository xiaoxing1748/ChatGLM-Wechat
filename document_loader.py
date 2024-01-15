# https://python.langchain.com/docs/modules/data_connection/document_loaders
import pprint
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_community.document_loaders import JSONLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
import os
from text_splitter import ChineseTextSplitter


# 通用加载器
def load(filepath):
    # 检测文件后缀
    _, ext = os.path.splitext(filepath)
    if ext in ['.json', '.jsonl']:
        return load_json(filepath)
    if ext in ['.csv']:
        return load_csv(filepath)
    else:
        return load_and_split_unstructured(filepath)


# JSONLoader 需要安装jq库(windows没有wheel故无法安装)
# 见https://python.langchain.com/docs/modules/data_connection/document_loaders/json
def load_json(filepath):
    """return data\n
    JSON文档加载器"""
    # 加载数据
    loader = JSONLoader(
        file_path=filepath,
        jq_schema='.messages[].content',
        text_content=False)
    data = loader.load()
    # pprint(data)
    return data


# csv加载器
# https://python.langchain.com/docs/integrations/document_loaders/csv
def load_csv(filepath):
    """return docs\n
    CSV文档分割器"""
    loader = CSVLoader(
        file_path=filepath,
        csv_args={
            "delimiter": ",",
            "quotechar": '"',
            "fieldnames": ["- ask", "answer"],
        },
    )
    data = loader.load()
    # print(data)
    return data


# 非结构化文档加载器 有下面的加载分割器就用不着这个了
def load_unstructured(filepath):
    """return docs\n
    非结构化文档加载器\n
    返回样式示例:\n
    [Document(page_content='你好', metadata={'source': ''})]"""
    # 加载数据
    loader = UnstructuredFileLoader(filepath)
    docs = loader.load()
    # print(docs)
    return docs


# 非结构化文档加载分割器
def load_and_split_unstructured(filepath):
    """return docs\n
    非结构化文档加载分割器\n
    返回样式示例(分割出几条有几条Document对象):\n
    [Document(page_content='你好', metadata={'source': ''}),Document(page_content='我好', metadata={'source': ''})]"""
    # 加载数据
    loader = UnstructuredFileLoader(filepath)
    text_splitter = ChineseTextSplitter()
    docs = loader.load_and_split(text_splitter=text_splitter)
    # print(docs)
    return docs


if __name__ == '__main__':
    # docs = load("./document/news.txt")
    docs = load("./knowledge_base/a.csv")
    print(docs)
