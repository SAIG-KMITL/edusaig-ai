import requests
from typing import List, Dict, Union
from langchain.text_splitter import RecursiveCharacterTextSplitter
from internal.LLMRequest import LLMRequest
        
    
class Summarization(LLMRequest):
    def SumText(self,text: str):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=12000,chunk_overlap=500)
        docs = text_splitter.create_documents([text])
        print(f"Total chunks : {len(docs)}")

        chunk_sum = []
        for i,chunk in enumerate(docs):
            prompt = (
                        f"Please summarize this text into one paragraph in the same language as the text."
                        f" The summarize must be less than 200 words : {chunk}"
                     )
            messages = [
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt},
                        ]
            sum = self.send_request(messages)
            if(not sum):
               print(f"Fail to summarize chunk {i}. Can not continue process.")
               return None
            #print(sum)
            print(f"chunk {i} done")
            chunk_sum.append(sum['choices'][0]['message']['content'] )
        
        combine_text = " ".join(chunk_sum)
        final_prompt = f"Please consider this text as 1 text and summarize it into bullet point: {combine_text}"
        messages = [
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": final_prompt},
        ]
        final_sum = self.send_request(messages)
        if(final_sum):
            print(final_sum['choices'][0]['message']['content'])
        return final_sum