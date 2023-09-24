# ChatGLM-Wechat
## 个人毕业设计：基于ChatGLM的微信公众号

​	碎碎念：requirement没写全，wechatpy库用的2.0.0alpha26，现成项目结构一团浆糊做完再整理，还在琢磨客服消息功能，假设无认证公众号则转为网页面板版（但这样就不能在答辩时唬住老师，谨慎选择）

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

- [ ] 训练个Lora（完成整体项目还能闲下来的话）

#### 架构功能：

- [ ] 改善提示词
- [ ] 优化逻辑，在启动项目时立刻使用读取并构建向量库
- [ ] 回复“/刷新”清除历史对话
- [ ] 对话记忆（显存不足以支撑多轮对话，仅供娱乐）

#### 面板功能：

- [ ] 管理知识库
- [ ] 切换模型和embeddings
- [ ] 问答功能
- [ ] 参数调节（分割和历史长度）
- [ ] 切换GPU（也许毫无意义）

------



### **参考内容：**

​	开发文档: [wechatpy官方文档](https://wechatpy.readthedocs.io/zh_CN/master/)

​	webui参考: [LangChain-ChatGLM-Webui](https://github.com/thomas-yanxin/LangChain-ChatGLM-Webui)

​	框架原理: [Langchain-Chatchat](https://github.com/chatchat-space/Langchain-Chatchat)

​	模型: [ChatGLM2-6B](https://github.com/THUDM/ChatGLM2-6B)
