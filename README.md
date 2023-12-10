# ChatGLM-Wechat
## 个人毕业设计：基于ChatGLM的微信公众号

------

### **项目结构（大饼）：**

```
ChatGLM-Wechat:.
├─config.yml #填写appid、secret、域、token
├─requirements.txt #依赖
├─Setup.py #项目首次启动安装依赖，然后启动main.py服务
├─wechatServer.py #服务器连接API
├─main.py #主服务
├─webUI.py #后台面板
├─document #知识库目录
|   └news.txt #知识库文件
└─model #本地模型目录
    └chatglm2-6b-int4 #单个模型的目录
```

------

### **Todo（大饼）：**

#### 模型功能：

- [ ] ~~训练个Lora（完成整体项目还能闲下来的话）~~  效果不佳，已放弃

#### 架构功能：还在做

- [ ] venv虚拟环境  鸽
- [x] 改善提示词
- [ ] 优化逻辑，在启动项目时立刻使用读取并构建向量库  在做了
- [ ] 回复“/刷新”清除历史对话  鸽
- [ ] 多轮对话  注：仅限api版

#### 面板功能：不重要总体先鸽

- [ ] 管理知识库
- [ ] 切换模型和embeddings
- [ ] 问答功能  鸽
- [ ] ~~参数调节（分割和历史长度）~~  不需要了
- [ ] ~~切换GPU（也许毫无意义）~~  用不着

#### 回复功能：

- [ ] 非认证公众号（响应时间五秒）

  发送问题后返回提示或快速回复按钮，提示发送“/获取回答”获取回答

- [x] 认证公众号（客服功能）

  发送问题后转接客服返回生成出的回答

- [ ] ~~备选方案（以上两种方式无法实现时）~~  不需要了

  跳转到页面使用网页问答功能

------



### **参考内容：**

​	开发文档: [wechatpy官方文档](https://wechatpy.readthedocs.io/zh_CN/master/)

​	webui参考: [LangChain-ChatGLM-Webui](https://github.com/thomas-yanxin/LangChain-ChatGLM-Webui)

​	框架原理: [Langchain-Chatchat](https://github.com/chatchat-space/Langchain-Chatchat)

​	模型: [ChatGLM2-6B](https://github.com/THUDM/ChatGLM2-6B)
