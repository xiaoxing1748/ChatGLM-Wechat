from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from transformers import AutoTokenizer, AutoModel
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
import sentence_transformers

# 启动模型
tokenizer = AutoTokenizer.from_pretrained(
    r"F:\ChatGLM2-6B\model", trust_remote_code=True)
model = AutoModel.from_pretrained(
    r"F:\ChatGLM2-6B\model", trust_remote_code=True).cuda()
chatglm = model.eval()


# 自定义路径
filepath = "./docs/news.txt"

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

# 根据提问匹配上下文
query = "总结一下本游戏攻略的内容"
docs = vector_store.similarity_search(query)
context = [doc.page_content for doc in docs]

# 构造Prompt
prompt = f"已知信息:\n{context}\n根据已知信息,用简短的话回答问题:\n{query}"
print(format(prompt))

# 生成回答
response, history = chatglm.chat(tokenizer, prompt, history=[])
print("回答:",response)
