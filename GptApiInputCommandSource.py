import json
import os

from openai import OpenAI

GPT_VERSION = "gpt-4-1106-preview"

class GptApiInputCommandSource:

    messageList = [{"role": "system", "content": "You are an agent controlling boiling a kettle. "
                                              "Try to boil the kettle as efficiently as possible."}]
    tools = [
        {
            "type" : "function",
            "function" : {
                "name" : "heat",
                "description" : "start heating"
            }
        },
        {
            "type" : "function",
            "function" : {
                "name" : "standby",
                "description" : "stop heating"
            }
        },
        {
            "type" : "function",
            "function" : {
                "name" : "status",
                "description" : "get the elapsed time, temperature and heating status of the kettle"
            }
        },
        {
            "type" : "function",
            "function" : {
                "name" : "sleep",
                "description" : "ask to be woken up after a given amount seconds to be asked for a new command",
                "parameters" : {
                    "type" : "object",
                    "properties" : {
                        "seconds" : {
                            "type" : "integer",
                            "description" : "the number of seconds to be woken after, to be asked for a new response"
                        }
                    },
                    "required" : ["seconds"]
                }
            }
        },
        {
            "type" : "function",
            "function" : {
                "name" : "quit",
                "description": "request the agent be shut down when all tasks have been completed"
            }
        }
    ]

    def __init__(self):
        # NOTE - you'll have to have set up an OPENAI_API_KEY first, for the next line to pick it up
        self.client = OpenAI()

    def generate_command(self, promptOrFunctionResponse: str):
        # NOTE - hacky setup - we need to check if the previous call was a function, and create a tool call
        #  response with the id

        if len(self.messageList) <= 1:
            print("\n\nCalling GPT API with initial prompt '", promptOrFunctionResponse, "'")
            self.messageList.append({"role": "user", "content": promptOrFunctionResponse})
        else:
            print("\n\nCalling GPT API with response from kettle '", promptOrFunctionResponse, "'", sep="")
            previous_function_call = self.messageList[-1].tool_calls[0]
            self.messageList.append({"role" : "tool",
                                     "tool_call_id": previous_function_call.id,
                                     "name" : previous_function_call.function.name,
                                     "content": promptOrFunctionResponse})

        chat_completion = self.client.chat.completions.create(messages=self.messageList, model=GPT_VERSION, tools=self.tools)

        print(chat_completion.choices[0].message)

        generated_message = chat_completion.choices[0].message
        self.messageList.append(generated_message)

        if generated_message.tool_calls is not None:

            function = generated_message.tool_calls[0].function
            function_name = function.name
            print("Response from GPT API (tool call):", function_name)
            if len(function.arguments) > 2:
                arguments_json_object = json.loads(function.arguments)
                return (function_name, arguments_json_object['seconds']) # hack
            else:
                return (function_name, None)
        else:
            print("Response from GPT API (text message) ", generated_message.content)
            return (generated_message.content, None)

