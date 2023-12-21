from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
from typing import Any
import os
import json

from openai.types.chat.chat_completion import ChatCompletion, ChatCompletionMessage


class MessageItem:
    def __init__(self, role: str, content: str | Any):
        self.role: str = role
        self.content: str | Any = content   

class OpenAIBot:
    def __init__(self, model: str = "gpt-3.5-turbo-1106") -> None:
        self.model: str = model
        load_dotenv(find_dotenv())
        # os.environ['OPENAI_API_KEY']  = "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"
        print(f"Open API KEY is {os.environ.get('OPENAI_API_KEY')}")
        
        self.client: OpenAI = OpenAI()

        self.messages: list[MessageItem] = []
        self.streams = []



    def send_message(self, prompt: str)->MessageItem:
        self.addMessage(MessageItem(role="user", content=prompt))
        
        response = self.run_conversation(prompt)
    
        m:MessageItem = MessageItem(role='assistant', content=response)
        # self.addMessage(m)
        return m

      
    def addMessage(self, message:MessageItem):
        self.messages.append(message)
    

    def getMessages(self)->list[MessageItem]:
        return self.messages
    
    def add_stream(self, stream):
        self.streams.append(stream)


    def run_conversation (self, main_request:str)->str:

        messages = [{"role": "user", "content": main_request}]
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_current_weather",
                    "description": "Get the current weather in a given location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city and state, e.g. San Francisco, CA",
                            },
                            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                        },
                        "required": ["location"],
                    },
                },
            }
        ]

        # First Request
        response: ChatCompletion = self.client.chat.completions.create(
            model = self.model,
            messages=messages,
            tools=tools,
            tool_choice="auto",  # auto is default, but we'll be explicit
            # stream=True,
        )

        # if response.choices[0].delta.tool_calls is None:
        #     full_response = ""
        #     for chunk in response:
        #         chunk_response = chunk
        #         if chunk.choices[0].delta.tool_calls is None:
        #             if chunk.choices[0].delta.content is not None:
        #                 full_response += chunk.choices[0].delta.content
        #                 yield chunk.choices[0].delta.content
                    
                
        #     self.addMessage(MessageItem(role='assistant', content=full_response))
        #     return full_response
        # else:
        
        response_message: ChatCompletionMessage = response.choices[0].message
        print("* First Response: ", dict(response_message))

        tool_calls = response_message.tool_calls
        # print("* First Reponse Tool Calls: ", list(tool_calls))

        # Step 2: check if the model wanted to call a function
        if tool_calls is not None:
            # Step 3: call the function
            # Note: the JSON response may not always be valid; be sure to handle errors
            available_functions = {
                "get_current_weather": get_current_weather,
            }  # only one function in this example, but you can have multiple
            
            messages.append(response_message)  # extend conversation with assistant's reply
            
            # Step 4: send the info for each function call and function response to the model
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                function_response = function_to_call(
                    location=function_args.get("location"),
                    unit=function_args.get("unit"),
                )
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )  # extend conversation with function response
            # print("* Second Request Messages: ", list(messages))
            second_response: ChatCompletion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True
            )  # get a new response from the model where it can see the function response


            full_response = ""
            for chunk in second_response:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    yield chunk.choices[0].delta.content

            self.addMessage(MessageItem(role='assistant', content=full_response))
            # print("* Second Response: ", dict(second_response))
            # print("* role: ", second_response.choices[0].message.role)
            return full_response
        

        

# end of class 
        
def get_current_weather(location:str, unit:str="fahrenheit")->str:
    """Get the current weather in a given location"""
    if "tokyo" in location.lower():
        return json.dumps({"location": "Tokyo", "temperature": "10", "unit": "celsius"})
    elif "san francisco" in location.lower():
        return json.dumps({"location": "San Francisco", "temperature": "72", "unit": "fahrenheit"})
    elif "paris" in location.lower():
        return json.dumps({"location": "Paris", "temperature": "22", "unit": "celsius"})
    else:
        return json.dumps({"location": location, "temperature": "unknown"})