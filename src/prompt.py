import openai
from data_extract import extract_type


def ner(prompt):
    response = openai.Completion.create(
        model="ada:ft-travelai-2023-06-06-23-12-58",
        prompt=f"""{prompt}\n\n###\n\n""",
        max_tokens=1000,
        temperature=0.2,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["###"],
    )

    # TODO: Geografia

    return extract_type(response["choices"][0]["text"])
