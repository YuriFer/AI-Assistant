from typing import Optional
from openai import OpenAI
import json
import os

from openai import OpenAI

from ia_prompt import INITIAL_PROMPT


class OpenAiRequest:
    def __init__(
        self,
        system_prompt: str,
        user_prompt: str,
        messages: list,
        json_mode: bool = False,
        model: str = os.getenv("OPENAI_MODEL"),
        temperature: float = 0.0,
        seed: Optional[int] = None,
    ):
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        self.messages = messages
        self.model = model
        self.temperature = temperature
        self.seed = seed
        self.json_mode = json_mode

class OpenAiResponse:
    def __init__(
            self,
            response:str
    ):
        self.response = response

class OpenAIService:
    def initiate_context(self, user_message: str, widget):
        system_prompt = INITIAL_PROMPT

        openai_request = OpenAiRequest(
            system_prompt=system_prompt,
            user_prompt=user_message,
            messages=[]
        )

        response =  self.execute_call_openai(openai_request, widget)
        return response

    def execute_call_openai(self, openai_request: OpenAiRequest, widget) -> OpenAiResponse:
        response_call = self.call_openai(
            openai_request.messages,
            openai_request.model,
            openai_request.temperature,
            openai_request.json_mode,
            openai_request.seed,
            widget
        )

        get_choices = OpenAiResponse(
            response=response_call
        )

        return get_choices


    def call_openai(
            self,
            messages: list,
            model: str = os.getenv("OPENAI_MODEL"),
            temperature: float = 0.0,
            json_mode: bool = False,
            seed: Optional[int] = None,
            widget=None
    ):
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
        response:str = ""

        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            seed=seed,
            stream=True,
        )

        widget.configure(state="normal")

        widget.delete("1.0", "end")

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                if widget is not None:
                    response += chunk.choices[0].delta.content
                    widget.insert("end", f"{chunk.choices[0].delta.content}")
                    widget.update_idletasks()
        
        widget.insert("end", "\n")
        widget.configure(state="disabled")

        if json_mode:
            return json.loads(response)
        return response