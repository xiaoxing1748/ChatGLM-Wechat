from fastapi import FastAPI, Request
from transformers import AutoTokenizer, AutoModel
import uvicorn
import json
import datetime
import torch
import requests
from config_loader import ConfigLoader as config
DEVICE = "cuda"
DEVICE_ID = "0"
CUDA_DEVICE = f"{DEVICE}:{DEVICE_ID}" if DEVICE_ID else DEVICE


def torch_gc():
    if torch.cuda.is_available():
        with torch.cuda.device(CUDA_DEVICE):
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()


app = FastAPI()


@app.post("/")
async def create_item(request: Request):
    global model, tokenizer
    json_post_raw = await request.json()
    json_post = json.dumps(json_post_raw)
    json_post_list = json.loads(json_post)
    prompt = json_post_list.get('prompt')
    history = json_post_list.get('history')
    max_length = json_post_list.get('max_length')
    top_p = json_post_list.get('top_p')
    temperature = json_post_list.get('temperature')
    response, history = model.chat(tokenizer,
                                   prompt,
                                   history=history,
                                   max_length=max_length if max_length else 2048,
                                   top_p=top_p if top_p else 0.7,
                                   temperature=temperature if temperature else 0.95)
    now = datetime.datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    answer = {
        "response": response,
        "history": history,
        "status": 200,
        "time": time
    }
    log = "[" + time + "] " + '", prompt:"' + \
        prompt + '", response:"' + repr(response) + '"'
    print(log)
    torch_gc()
    return answer


# 启用llm服务
def run_llm(LLM_PATH=None):
    if LLM_PATH is None:
        LLM_PATH = config().get_llm_config("llm_path")
    global model, tokenizer
    tokenizer = AutoTokenizer.from_pretrained(LLM_PATH, trust_remote_code=True)
    model = AutoModel.from_pretrained(
        LLM_PATH, trust_remote_code=True).cuda()
    # 多显卡支持，使用下面三行代替上面两行，将num_gpus改为你实际的显卡数量
    # model_path = LLM_PATH
    # tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    # model = load_model_on_gpus(model_path, num_gpus=2)
    model.eval()
    uvicorn.run(app, host='0.0.0.0', port=8000, workers=1)


# 发送聊天请求
def chat(prompt, history=None, max_length=None, top_p=None, temperature=None):
    """return json \n {'response': \n'你好👋！我是人工智能助手 ChatGLM2-6B，很高兴见到你，欢迎问我任何问题。',\n 'history': \n[['你好', '你好👋！我是人工智能助手 ChatGLM2-6B，很高兴见到你，欢迎问我任何问题。']],\n 'status': 200,\n 'time': '2023-12-12 05:57:00'}
    """
    url = "http://localhost:8000/"
    json_payload = {
        "prompt": prompt,
        "history": history,
        "max_length": max_length,
        "top_p": top_p,
        "temperature": temperature
    }
    try:
        response = requests.post(url, json=json_payload)
        response.raise_for_status()
        result = response.json()
        print("Response:", result["response"])
        print("History:", result["history"])
        print("Status:", result["status"])
        print("Time:", result["time"])
        return result

    except requests.exceptions.RequestException as e:
        print(f"Error making chat request: {e}")
        return None


if __name__ == '__main__':
    LLM_PATH = config().get_llm_config("llm_path")
    run_llm(LLM_PATH)
