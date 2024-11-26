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
                        "Please summarize the following text into one concise paragraph"
                        "The summary should focus solely on the educational content and ignore irrelevant topics such as promotions or unrelated discussions. "
                        "The text must be less than 200 words."
                        f"Text: {chunk}"
                     )
            messages = [
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt},
                        ]
            sum = self.send_request(messages)
            if(not sum):
               print(f"Fail to summarize chunk {i}. Can not continue process.")
               return None
            #print(len(sum['choices'][0]['message']['content']))

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