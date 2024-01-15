import datetime
import time
from config_loader import ConfigLoader as config
import faiss_vector_store as faiss_vector_store
import knowledge_chain
import embeddings
import json
import qianfan_api as qianfan
import csv

print("启动于:", datetime.datetime.now())
config = config()
qfapikey = config.get_qianfan_config("apikey")
qfsecretkey = config.get_qianfan_config("secretkey")


# 初始化向量存储
def get_vector_store():
    # 加载embedding
    embedding = embeddings.load()
    # 向量存储
    return faiss_vector_store.index(document_path, embedding)


# 检索文档
def get_docs(question):
    return faiss_vector_store.search(question, document_path, vector_store)


# 文档路径
document_path = "./knowledge_base/本地知识库.csv"
# 向量存储
vector_store = get_vector_store()


def process_data():
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

                answer = get_docs(response)[0]
                print(answer[0].page_content.split("answer: ")[1])

                csv_writer.writerow(
                    [question, response, answer[0].page_content.split("answer: ")[1], execution_time_ms_rounded, answer[-1]])  # 写入output.csv
                print("写入成功")


process_data()
