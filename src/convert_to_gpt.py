from utils import load_data, save_jsonl

data = load_data("training_data/training_set.json")

class Prompt:
    def __init__(self, prompt, completion):
        self.prompt = prompt
        self.completion = completion
    def __str__(self):
        return f'{self.prompt},{self.completion}'

def convert(data):
    prompts = []
    for datum in data:
        ents = datum[1]
        completion  = ""
        for ent in ents["entities"]:
            completion += f'{ent[2]}: [\'{datum[0][ent[0]:ent[1]]}\']\n'
        training_prompt = Prompt(f'{datum[0]} \n\n###\n\n',f'{completion}END')
        prompts.append(training_prompt)
    return(prompts)

print(type(convert(data)))
save_jsonl("training_data/training_gpt.jsonl",convert(data))