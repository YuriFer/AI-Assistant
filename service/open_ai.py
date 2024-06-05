from typing import Optional
from openai import OpenAI
import json
import os
import datetime

from openai import OpenAI

from dengue_api_consult import ApiRequestObject, DengueApiService
from ia_prompt import INITIAL_PROMPT, TOOLS, INITIAL_TOOL_PROMPT

openai_request = None
widget_response = None
now = (
    datetime.datetime.now()
    .replace(hour=0, minute=0, second=0)
    .strftime("%d/%m/%Y")
)
class OpenAiRequest:
    def __init__(
        self,
        system_prompt: str,
        user_prompt: str,
        json_mode: bool = False,
        model: str = os.getenv("OPENAI_MODEL"),
        temperature: float = 0.0,
        tools: Optional[str] = None,
        tool_choice: Optional[str] = "auto",
        seed: Optional[int] = None,
        stream: bool = True
    ):
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        self.messages = messages
        self.model = model
        self.temperature = temperature
        self.tools = tools
        self.tool_choice = tool_choice
        self.seed = seed
        self.json_mode = json_mode
        self.stream = stream


class OpenAiResponse:
    def __init__(
            self,
            id: str,
            object: str,
            created: int,
            model: str,
            choices: list
    ):
        self.id = id
        self.object = object
        self.created = created
        self.model = model
        self.choices = choices

class OpenAIService:
    def execute_conversation(self, user_message: str, widget):
        global openai_request, widget_response
        widget_response = widget

        try:
            if openai_request:
                user_question = {"role": "user", "content": user_message}
                openai_request.messages.append(user_question)
            else:
                openai_request = OpenAiRequest(
                    system_prompt=INITIAL_TOOL_PROMPT.format(date=now), 
                    user_prompt=user_message, 
                    tools=TOOLS
                )
                conversation_history = openai_request.messages
            
            response: OpenAiResponse = self.execute_call_openai(openai_request)
            conversation_history.append(response.choices)

        except Exception as e:
            print(e)
            response = None

    
    def execute_call_openai(self, openai_request: OpenAiRequest) -> OpenAiResponse:
        response_call:OpenAiResponse = self.call_openai(openai_request)

        message = response_call.choices

        if "tool_calls" in message and message.get('tool_calls') is not None:
            tool_name = message["tool_calls"][0].function.name

            if tool_name == "SPECIFIC_SEARCH":
                arguments = json.loads(message["tool_calls"][0].function.arguments)

                dengue_api = DengueApiService()

                geocode_city = dengue_api.load_cities(arguments["city"])
                disease = arguments["disease"]
                start_week, end_week, start_year, end_year = dengue_api.transform_date(arguments["start_date"], arguments["end_date"])

                api_request = ApiRequestObject(geocode=geocode_city, week_start=start_week, week_end=end_week, year_start=start_year, year_end=end_year, disease=disease)
                
                dengue_api_response = dengue_api.call_dengue_api(api_request)

                print(dengue_api_response)

            # elif tool_name == "GENERAL_SEARCH":
            #     print("GENERAL_SEARCH")
            #     user_question = json.loads(message["tool_calls"][0].function.arguments)
        else:
            print("SEM FERRAMENTA")
            print(response_call)
        
        return response_call


    def call_openai(self, openai_request: OpenAiRequest):
        """
        Call the OpenAI API with a list of messages and return the response.

        :param messages: List of messages to send to the API.
        :param model: The model to use for the API.
        :param temperature: The temperature to use for the API.
        :param json_mode: Whether to return the response as JSON.
        :param seed: The seed to use for the API.
        :return: The response from the API.
        """
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        content:str = ""
        arguments:str = ""
        first_chunk = None

        client_response = client.chat.completions.create(
            model=openai_request.model,
            messages=openai_request.messages,
            temperature=openai_request.temperature,
            seed=openai_request.seed,
            tools=openai_request.tools,
            tool_choice=openai_request.tool_choice,
            stream=openai_request.stream
        )

        if client_response is not None:
            first_chunk = next(client_response)
            for chunk in client_response:
                content += chunk.choices[0].delta.content if chunk.choices[0].delta.content is not None else ""
                if chunk.choices[0].delta.tool_calls is not None:
                    arguments += chunk.choices[0].delta.tool_calls[0].function.arguments if chunk.choices[0].delta.tool_calls[0].function.arguments is not None else ""
                if chunk.choices[0].delta.content is not None:
                    self.show_response(chunk)
            
                    widget_response.insert("end", "\n")
                    widget_response.configure(state="disabled")

            first_chunk.choices[0].delta.content = content
            first_chunk.choices[0].delta.tool_calls[0].function.arguments = arguments

            response = OpenAiResponse(
                id=first_chunk.id,
                object=first_chunk.object,
                created=first_chunk.created,
                model=first_chunk.model,
                choices=first_chunk.choices[0].delta.__dict__
            )
        else:
            return None

        return response

            
    def show_response(self, chunk):
        widget_response.configure(state="normal")
        widget_response.delete("1.0", "end")
        widget_response.insert("end", f"{chunk.choices[0].delta.content}")
        widget_response.update_idletasks()