from openai import OpenAI
from openai.types.beta import Assistant
from openai.types.beta.thread import Thread
from openai.types.beta.threads.thread_message import ThreadMessage
from openai.types.beta.threads.run import Run

from dotenv import load_dotenv, find_dotenv
from typing import Any
import os
import json
import time



class MessageItem:
    def __init__(self, role: str, content: str | Any):
        self.role: str = role
        self.content: str | Any = content   

class OpenAIBot:
    def __init__(self, name:str, instructions: str, model: str = "gpt-3.5-turbo-1106") -> None:
        
        self.name = name
        self.instructions = instructions
        self.model: str = model

        load_dotenv(find_dotenv())
        print(f"Open API KEY is {os.environ.get('OPENAI_API_KEY')}")

        self.client: OpenAI = OpenAI()
        self.assistant: Assistant = self.client.beta.assistants.create(
            name= self.name,
            instructions= self.instructions,
            tools=[{"type": "code_interpreter"}],
            model=self.model
        )
        
        self.thread: Thread = self.client.beta.threads.create()
        self.messages: list[MessageItem] = []
        self.streams = []



    def send_message(self, prompt: str)->str:
        # self.addMessage(MessageItem(role="user", content=prompt))
        
        
        message = self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=prompt,
        )
        print(f"Message ", message)

        self.latest_run: Run = self.client.beta.threads.runs.create(
            thread_id= self.thread.id,
            assistant_id= self.assistant.id,
            instructions= self.instructions
        )
        print(f"Message => : ", message.content[0].text.value)
        print(f"Role => : ", message.role)
        
        
        self.addMessage(MessageItem(role=message.role, content=message.content[0].text.value))

        # run: Run = self.client.beta.threads.runs.retrieve(
        #     thread_id= self.thread.id,
        #     run_id= run.id,
        # )

        # messages: list[ThreadMessage] = self.client.beta.threads.messages.list(
        #     thread_id=self.thread.id
        #     )
        # print(f"Messages ", messages)


        # for m in reversed(messages.data):
        #     print(m.role + ": " + m.content[0].text.value)



    def isCompleted(self)->bool:
        print("Status: ", self.latest_run.status)
        while self.latest_run.status != "completed":
            print("Going to sleep")
            time.sleep(1)
            self.latest_run : Run = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread.id,
                run_id=self.latest_run.id
            )
            print("Latest Status: ", self.latest_run.status)
            # print("Latest Run: ", self.latest_run)
        return True
    
      
    def addMessage(self, message:MessageItem):
        self.messages.append(message)
    

    def getMessages(self)->list[MessageItem]:
        return self.messages
    
    def add_stream(self, stream):
        self.streams.append(stream)

    def get_lastest_response(self)-> MessageItem:
        messages = self.client.beta.threads.messages.list(
            thread_id=self.thread.id
        )
        print("Response: ", messages.data[0])
        m = MessageItem(messages.data[0].role, messages.data[0].content[0].text.value)
        self.addMessage(m)
        return m

# end of class 