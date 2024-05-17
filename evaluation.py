import datetime
import time
from config_loader import ConfigLoader as config
import faiss_vector_store as faiss_vector_store
import knowledge_chain
import embeddings
import json
import qianfan_api as qianfan
import csv
from langchain_community.vectorstores import FAISS
import embeddings
from langchain_community.document_loaders.csv_loader import CSVLoader
import os

print("启动于:", datetime.datetime.now())
config = config()
qfapikey = config.get_qianfan_config("apikey")
qfsecretkey = config.get_qianfan_config("secretkey")


# 用于回答检索的向量库初始化方法 每一行需要包含ask和answer两列及表头
def get_vector_store(filepath):
    # 加载embedding
    embedding = embeddings.load()
    # 向量存储
    return faiss_vector_store.index(filepath, embedding)


# 分析结果用的向量库初始化方法 其中参考回答文档需要预处理至仅有回答列 建议用简短的表头
def get_vector_store1(filepath):
    embedding = embeddings.load()
    loader = CSVLoader(
        file_path=filepath,
        csv_args={
            "delimiter": ",",
            "quotechar": '"',
        }
    )
    data = loader.load()
    return FAISS.from_documents(data, embedding)


# 检索文档
def get_docs(question, vector_store):
    docs = vector_store.similarity_search_with_score(question)
    return docs


# 文档路径
document_path = "./backup/本地知识库.csv"
answer_sets = "./backup/参考回答.csv"


# 改进的测试方式
def process_data():
    vector_store = get_vector_store(document_path)
    # 打开输入和输出文件
    with open('input.csv', mode='r', encoding='gb2312') as infile, open('output.csv', mode='w', encoding='utf-8', newline='') as outfile:
        csv_reader = csv.reader(infile)
        csv_writer = csv.writer(outfile)
        # 读取input.csv每一行
        for row in csv_reader:
            if row:  # 检查行不是空的
                question = row[0]  # 获取第一列的字符串
                print(question)
                # 开始计时
                start_time = time.time()
                # 本地知识库QA链
                response = knowledge_chain.qa_chain(question, vector_store)
                # # 千帆知识库QA链
                # response = knowledge_chain.qianfan_qa_chain(
                #     qfapikey, qfsecretkey, question, vector_store)
                # # 千帆知识库
                # response = qianfan.chat_with_knowledge_base(question).text
                # response = json.loads(response)["result"]
                print(response)
                # 结束计时
                end_time = time.time()
                execution_time_ms = (end_time - start_time) * 1000
                execution_time_ms_rounded = round(execution_time_ms, 2)
                # 打印执行时长
                print(execution_time_ms_rounded)
                csv_writer.writerow(
                    [question, response, execution_time_ms_rounded])
                print("写入成功")


# 检索参考回答并评估
def analysis_data():
    vector_store = get_vector_store1(answer_sets)
    with open('output.csv', mode='r', encoding='utf-8') as infile, open('analysis.csv', mode='w', encoding='utf-8', newline='') as outfile:
        csv_reader = csv.reader(infile)
        csv_writer = csv.writer(outfile)
        for row in csv_reader:
            if row:  # 检查行不是空的
                question = row[0]
                response = row[1]
                # execution_time_ms_rounded = row[2]
                execution_time_ms_rounded = row[3]
                print(response)
                answers = get_docs(response, vector_store)
                # 取前三个最相关的进行手动评估
                answer1 = answers[0]
                answer2 = answers[1]
                answer3 = answers[2]
                csv_writer.writerow(
                    [question, response, execution_time_ms_rounded, answer1[0].page_content, answer1[-1], answer2[0].page_content, answer2[-1], answer3[0].page_content, answer3[-1]])  # 写入output.csv
                print("写入成功")


# process_data()
analysis_data()
