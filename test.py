import faiss_vector_store
import knowledge_chain
# vector_store = faiss_vector_store.index("./document/test.txt")
# question = "总结一下已知信息"
# print(knowledge_chain.llm_chain("你好"))
print(knowledge_chain.qa_chain_legacy(
    "你好", faiss_vector_store.index("./document/test.txt")))
