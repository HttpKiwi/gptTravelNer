import openai
import os
from src.data_extract import extract_type

api_key = os.environ["API_KEY"]
openai.api_key = api_key


def ner(prompt):
    response = openai.Completion.create(
        model="ada:ft-travelai:full-ner-2023-06-20-07-42-31",
        prompt=f"""{prompt}\n\n###\n\n""",
        max_tokens=1000,
        temperature=0.2,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\n###"],
    )
    print(response["choices"][0]["text"])
    return extract_type(response["choices"][0]["text"])


def people_ner(prompt):
    response = openai.Completion.create(
        model="ada:ft-travelai:people-ner-2023-06-19-01-37-21",
        prompt=f"""{prompt}\n\n###\n\n""",
        max_tokens=1000,
        temperature=0.2,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\n###"],
    )
    return extract_type(response["choices"][0]["text"])

def origin_ner(prompt):
    response = openai.Completion.create(
        model="ada:ft-travelai:origin-ner-2023-06-18-07-56-21",
        prompt=f"""{prompt}\n\n###\n\n""",
        max_tokens=1000,
        temperature=0.2,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\n###"],
    )
    return extract_type(response["choices"][0]["text"])

def duration_ner(prompt):
    response = openai.Completion.create(
        model="ada:ft-travelai:duration-ner-2023-06-18-22-37-52",
        prompt=f"""{prompt}\n\n###\n\n""",
        max_tokens=1000,
        temperature=0.2,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\n###"],
    )
    return extract_type(response["choices"][0]["text"])

def dates_ner(prompt):
    response = openai.Completion.create(
        model="ada:ft-travelai:dates-ner-2023-06-18-22-13-01",
        prompt=f"""{prompt}\n\n###\n\n""",
        max_tokens=1000,
        temperature=0.2,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\n###"],
    )
    return extract_type(response["choices"][0]["text"])

def budget_ner(prompt):
    response = openai.Completion.create(
        model="ada:ft-travelai:budget-ner-2023-06-20-06-20-37",
        prompt=f"""{prompt}\n\n###\n\n""",
        max_tokens=1000,
        temperature=0.2,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\n###"],
    )
    return extract_type(response["choices"][0]["text"])