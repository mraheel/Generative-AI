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
        load_dotenv(find_dotenv()) 
        self.client: OpenAI = OpenAI()
        self.messages: list[MessageItem] = []


    def send_message(self, prompt: str):
        self.addMessage(MessageItem(role="user", content=prompt))
        
        response : ChatCompletion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-3.5-turbo-1106",
        )
        response =  response.choices[0].message

        self.addMessage(MessageItem(role=response.role, content=response.content))
        return response


    def isCompleted(self)->bool:
        
        return True

    
    def addMessage(self, message:MessageItem):
        self.messages.append(message)
    

    def getMessages(self)->list[MessageItem]:
        return self.messages