# edusaig-ai

AI modules for edusaig

How to run ?


## 1. Create .env file

```
SAIG_LLM_URL = <input_value_here>
SAIG_LLM_URL_LANGCHAIN = xxxx/xxxx/v1
SAIG_LLM_MODEL = meta-llama/Meta-Llama-3.1-8B-Instruct
HUGGING_FACE_API_KEY = <input_value_here>
HUGGING_FACE_ASR_MODEL = https://api-inference.huggingface.co/models/openai/whisper-large-v3-turbo
```

## 2. Install Dependecies

```
pip install -r requirements.txt
```

## 3. Start FastAPI

```
uvicorn app:app --reload
```


## How we dev ?
if you have new service like "Chatbot Service"
1. Create router in routers folder.
2. Create Schema in  models folder.
3. Create Service in internal folder.



