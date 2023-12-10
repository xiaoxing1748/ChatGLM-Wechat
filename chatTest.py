from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from transformers import AutoTokenizer, AutoModel
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
import sentence_transformers

# 启动模型
tokenizer = AutoTokenizer.from_pretrained(
    r"F:\ChatGLM\model", trust_remote_code=True)
model = AutoModel.from_pretrained(
    r"F:\ChatGLM\model", trust_remote_code=True).cuda()
model = model.eval()

# 自定义路径
# filepath = "./document/news.txt"
filepath = "./document/data1.txt"

# 加载数据
loader = UnstructuredFileLoader(filepath)
docs = loader.load()

# 文本分割
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=200)
docs = text_splitter.split_documents(docs)

# 构建向量库
# embeddings = OpenAIEmbeddings()
embeddings_model_name = "shibing624/text2vec-base-chinese"
embeddings = HuggingFaceEmbeddings(
    model_name=embeddings_model_name)
embeddings.client = sentence_transformers.SentenceTransformer(
    embeddings.model_name, device="cuda:0")
vector_store = FAISS.from_documents(docs, embeddings)


def chat(question):
    # 根据提问匹配上下文
    # question = "博德之门3是什么？"
    docs = vector_store.similarity_search(question)
    context = [doc.page_content for doc in docs]

    # 构造Prompt
    prompt = f"现在你是招生答疑助手，你会结合已知的知识，为用户解答一些问题。你的任务是做一名问答助手，根据【检索结果】来回答最后的【问题】。在回答问题时，你需要注意以下几点：1.【检索结果】有多条，每条【检索结果】之间由一对ask与answer组成。2.如果某条【检索结果】与【问题】无关，就不要参考这条【检索结果】。3.请直接回答问题，不要强调客服的职责。【检索结果】:{context}【问题】:{question}"
    # prompt = question
    with open("./document/prompt.txt", "r", encoding="utf-8") as f:
        prompt1 = f.read()
    print(format(prompt1))

    # 生成回答
    response, history = model.chat(tokenizer, prompt, history=[])
    # print("回答:",response)
    return response


print(chat("跟我说说今年的信息"))
