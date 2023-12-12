import pprint
from langchain.document_loaders import UnstructuredFileLoader
from langchain.document_loaders import JSONLoader
import os
# from text_splitter.chinese_text_splitter import ChineseTextSplitter


# 通用加载器


def load(filepath):
    # 检测文件后缀
    _, ext = os.path.splitext(filepath)
    if ext in ['.json', '.jsonl']:
        return load_json(filepath)
    else:
        return load_unstructured(filepath)


#  JSONLoader 需要安装jq库(windows没有wheel故无法安装)
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


# 非结构化文档加载器
def load_unstructured(filepath):
    """return docs\n
    非结构化文档加载器"""
    # 加载数据
    loader = UnstructuredFileLoader(filepath)
    docs = loader.load()
    # print(docs)
    return docs


if __name__ == '__main__':
    text = load("./document/news.txt")
    # text = [Document(page_content='问：今天星期几\n\n答：星期三\n\n问：今天几度\n\n答：18度\n\n问：什么啤酒好喝\n\n答：哈尔滨\n\n问：丁真\n\n答：我测你们码', metadata={'source': './document/news.txt'})]
    # splitter = ChineseTextSplitter()
    # a = splitter.split_text(text[0].page_content)
    # print(a)
