# from openai import OpenAI, OpenAIError
# import os

# class CallOpenAI:
#     def __init__(self):
#         self.api_model = str(os.getenv("OPENAI_MODEL"))
#         self.api_key = str(os.getenv("OPENAI_API_KEY"))

#     def calling_openai(self):
#         client = OpenAI(api_key=self.api_key)

#         stream = client.chat.completions.create(
#             model=self.api_model,
#             messages=[{"role": "user", "content": "Say this is a test"}],
#             stream=True,
#         )

#         for chunk in stream:
#             if chunk.choices[0].delta.content is not None:
#                 print(chunk.choices[0].delta.content, end="")

# call = CallOpenAI()

# call.calling_openai()

# import the OpenAI Python library for calling the OpenAI API
from openai import OpenAI
import json
import os

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

stream = client.chat.completions.create(
    model=str(os.getenv("OPENAI_MODEL")),
    messages=[{"role": "user", "content": "Me conte uma história de no máximo 20 linhas"}],
    stream=True,
)
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")