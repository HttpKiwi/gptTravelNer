import openai
import os
from src.data_extract import extract_type

api_key = os.environ["API_KEY"]
openai.api_key = api_key


def ner(prompt):
    response = openai.Completion.create(
        model="ada:ft-travelai-2023-06-12-16-29-55",
        prompt=f"""{prompt}\n\n###\n\n""",
        max_tokens=1000,
        temperature=0.2,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\n###"],
    )

    # TODO: Geografia
    print(response["choices"][0]["text"])
    return extract_type(response["choices"][0]["text"])
