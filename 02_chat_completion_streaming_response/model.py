from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
from typing import Any
import os
from openai.types.chat.chat_completion import ChatCompletion

class MessageItem:
    def __init__(self, role: str, content: str | Any):
        self.role: str = role
        self.content: str | Any = content   

class OpenAIBot:
    def __init__(self, model: str = "gpt-3.5-turbo-1106") -> None:
        self.model: str = model
        # self.stram: str = True
        load_dotenv(find_dotenv()) 
        print(f"Open API KEY is {os.environ.get('OPENAI_API_KEY')}")
        self.client: OpenAI = OpenAI()
        self.messages: list[MessageItem] = []
        self.streams = []



    def send_message(self, prompt: str):
        self.addMessage(MessageItem(role="user", content=prompt))
        response : ChatCompletion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=self.model,
            stream=True
        )
        

        full_response = ""

        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
                yield chunk.choices[0].delta.content
        
    
        self.addMessage(MessageItem(role='assistant', content=full_response))
        return True

      
    def addMessage(self, message:MessageItem):
        self.messages.append(message)
    

    def getMessages(self)->list[MessageItem]:
        return self.messages
    
    def add_stream(self, stream):
        self.streams.append(stream)