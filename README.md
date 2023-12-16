# ChatGLM-Wechat

## 个人毕业设计：基于 ChatGLM 的微信公众号

---

### **项目结构（大饼）：**

```
ChatGLM-Wechat:.
├─config.yaml #配置
├─requirements.txt #依赖
├─Setup.py #项目首次启动安装依赖，然后启动main.py服务
├─wechat_api.py #服务器连接API
├─main.py #主服务
├─document #知识库目录
|   └news.txt #知识库文件
├─models #本地LLM模型目录
|   └chatglm2-6b-int4 #单个模型的目录
├─embeddings #本地Embedding模型目录
|   └bge-large-zh-v1.5 #单个模型的目录
|
├─config_loader.py #配置加载器
├─qianfan_api.py #千帆api
├─chatglm_api.py #chatglm api
├─document_loader.py #文档加载器
├─text_splitter.py #文本分割器
├─embeddings.py #嵌入加载器
├─faiss_vector_store.py #faiss向量存储器
├─knowledge_chain.py #知识库链
└─llm.py #实例化的LLM
```

---

### **Todo（大饼）：**

#### 模型功能：

- [ ] ~~训练个 Lora（完成整体项目还能闲下来的话）~~ 效果不佳，已放弃

#### 架构功能：还在做

- [x] venv 虚拟环境 在做了
- [x] 改善提示词
- [ ] ~~多轮对话 仅限 api 版~~  多轮对话费钱不做了
- [x] 改进配置功能

#### 问答功能：

- [x] 本地知识库+云端模型
- [x] 本地知识库+本地模型
- [x] 云端知识库+云端模型

#### ~~面板功能：~~  全鸽了

- [ ] ~~管理知识库~~
- [ ] ~~切换模型和 embeddings~~
- [ ] ~~问答功能~~
- [ ] ~~参数调节（分割和历史长度）~~
- [ ] ~~切换 GPU（也许毫无意义）~~

#### 回复功能：

- [x] 非认证公众号（响应时间五秒）

  发送问题后返回提示或快速回复按钮，提示发送“/获取回答”获取回答

- [x] 认证公众号（客服功能）

  发送问题后转接客服返回生成出的回答

- [ ] ~~备选方案（以上两种方式无法实现时）~~ 不需要了

  跳转到页面使用网页问答功能

---

### **参考内容：**

 开发文档: [wechatpy 官方文档](https://wechatpy.readthedocs.io/zh_CN/master/)

 webui 参考: [LangChain-ChatGLM-Webui](https://github.com/thomas-yanxin/LangChain-ChatGLM-Webui)

 框架原理: [Langchain-Chatchat](https://github.com/chatchat-space/Langchain-Chatchat)

 模型: [ChatGLM2-6B](https://github.com/THUDM/ChatGLM2-6B)
