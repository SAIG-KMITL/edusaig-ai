import requests
from typing import List, Dict, Union
from langchain.text_splitter import RecursiveCharacterTextSplitter

class LLMRequest:
    def __init__(self, url: str, model: str, max_tokens: int = 1024, temperature: float = 0.6, top_p: float = 0.95, repetition_penalty: float = 1.05, stop: List[str] = None):
        self.url = url
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.repetition_penalty = repetition_penalty
        self.stop = stop or ["<|im_end|>", "<|im_start|>", "<|eot_id|>"]
        self.headers = {
            "Content-Type": "application/json",
            # "Authorization": "Bearer YOUR_ACCESS_TOKEN",
        }

    def send_request(self, messages: List[Dict[str, str]], stream: bool = False) -> Union[Dict, None]:
        data = {
            "messages": messages,
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "repetition_penalty": self.repetition_penalty,
            "stop": self.stop,
            "stream": stream,
        }
        
        try:
            response = requests.post(self.url, json=data, headers=self.headers)
            response.raise_for_status()  # Check for HTTP errors
            
            # Parse and return JSON response if available
            return response.json() if response.status_code == 200 else None
            
        except requests.exceptions.RequestException as e:
            print("An error occurred:", e)
            return None
        
    def SumText(self,text: str):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000,chunk_overlap=500)
        docs = text_splitter.create_documents([text])

        chunk_sum = []
        for i,chunk in enumerate(docs):
            prompt = f"please summarize this text into one paragraph in original language and less than 300 words : {chunk}"

            messages = [
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt},
                        ]
            sum = self.send_request(messages)['choices'][0]['message']['content'] 
            print(sum)
            print(f"chunk {i} done")
            chunk_sum.append(sum)
        
        combine_text = " ".join(chunk_sum)
        final_prompt = f"please summarize this text into bullet point: {combine_text}"
        messages = [
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": final_prompt},
        ]
        final_sum = self.send_request(messages)
        print(final_sum)
        return final_sum