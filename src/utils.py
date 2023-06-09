import json
from rapidfuzz import process


def find_closest_object(input_str, json_list, key):
    choices = [obj[key] for obj in json_list]
    closest_match = process.extractOne(input_str, choices)
    closest_index = closest_match[2]
    closest_object = json_list[closest_index]
    return closest_object


def save_data(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def load_data(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def save_jsonl(file, data):
    with open(file, "w") as f:
        for item in data:
            f.write(f"{json.dumps(item.__dict__)} \n")
