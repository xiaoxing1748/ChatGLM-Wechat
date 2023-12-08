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
filepath = "./document/news.txt"

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


def chat(query):
    # 根据提问匹配上下文
    # query = "本次对话总共产生了多少tokens？以及为什么是这么多，你如何统计出来的？"
    docs = vector_store.similarity_search(query)
    context = [doc.page_content for doc in docs]

    # 构造Prompt
    prompt = f"已知信息:\n{context}\n根据已知信息,回答问题:\n{query}"
    print(format(prompt))

    # 生成回答
    response, history = model.chat(tokenizer, prompt, history=[])
    # print("回答:",response)
    return response
