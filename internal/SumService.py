import requests
from typing import List, Dict, Union

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