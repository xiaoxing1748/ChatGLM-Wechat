# import faiss_vector_store
# import knowledge_chain
# vector_store = faiss_vector_store.index("./document/test.txt")
# question = "总结一下已知信息"
# print(knowledge_chain.llm_chain("你好"))
# print(knowledge_chain.qa_chain_legacy(
# "你好", faiss_vector_store.index("./document/test.txt")))
import json

# JSON字符串
json_string = '{"id":"as-h6imfd0j38","object":"chat.completion","created":1702764497,"result":"我推荐尝试哈尔滨啤酒，这是一种口感清爽、带有麦芽香气的好啤酒。当然，每个人的口味偏好不同，你可以尝试不同的啤酒，找到自己喜欢的口感。","is_truncated":false,"need_clear_history":false,"usage":{"prompt_tokens":189,"completion_tokens":33,"total_tokens":222}}'

# 解析JSON字符串
data = json.loads(json_string)

# 提取"result"字段的值
result_value = data["result"]

# 打印"result"字段的值
# print(result_value)
print(json.loads(json_string)["result"])
