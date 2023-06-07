from utils import save_jsonl, load_data
import random

verbs = load_data("data/verb.json")
people = load_data("data/people.json")
places = load_data("data/place.json")
events = load_data("data/event.json")
airlines = load_data("data/airline.json")
modifiers = load_data("data/modifier.json")
months = load_data("data/month.json")
ammenities = load_data("data/ammenity.json")
hosting_verb = load_data("data/hosting_verb.json")
dates = load_data("data/date.json")


class Prompt:
    def __init__(self, prompt, completion):
        self.prompt = prompt
        self.completion = completion

    def __str__(self):
        return f"{self.prompt},{self.completion}"


def coin_flip():
    return bool(random.randint(0, 1))


def get_random(arr):
    return arr[random.randint(0, len(arr) - 1)]["value"]


def get_random_people():
    completion = ""
    people_string = ""
    needs_more_info = False
    amount = random.randint(1, 3)

    for n in range(1, amount):
        rand_people = random.choice(people)
        person, value = rand_people["value"], rand_people["amount"]
        if n == 1:
            people_string += "con mi"
        if n == amount - 1 and amount > 1:
            people_string += " y"
        people_string += f" {person},"
        if value == -1:
            needs_more_info = True
        completion += f"PERSON: ['{person}']\n"
    return people_string, completion, needs_more_info


def complete_people():
    completion = ""
    complete_string = ""
    if coin_flip():
        adults = random.randint(1, 8)
        children = random.randint(0, 8)
        infants = random.randint(0, 2)

        completion += f"ADULTS: ['{adults}']\n"
        complete_string += f"{adults} adultos, "
        if children > 0:
            complete_string += f"{children} niños, "
            completion += f"CHILDREN: ['{children}']\n"
        if infants > 0:
            complete_string += f"y {infants} infantes"
            completion += f"INFANTS: ['{infants}']\n"

    return complete_string, completion


def ran_ammenities():
    ammenity_q = ""
    ammenity_arr = []
    for am in range(random.randint(0, 6)):
        if am == 0:
            ammenity_q = "con "
        temp_ammenity = get_random(ammenities)
        ammenity_q += f"{temp_ammenity}, "
        ammenity_arr.append(temp_ammenity)
    return ammenity_q, ammenity_completion(ammenity_arr)


def ammenity_completion(ammenities):
    completion = ""
    for am in ammenities:
        completion += f"AMMENITY: ['{am}']\n"
    return completion


def get_airline_string():
    if coin_flip():
        rand = [
            {"text": " con", "type": "include"},
            {
                "text": f" con cualquier aerolinea {get_random(modifiers)}",
                "type": "exclude",
            },
        ]
        rand_chosen = random.choice(rand)
        airline_string, airline_type = rand_chosen["text"], rand_chosen["type"]
        completion_airline = ""
        completion_type = ""
        for am in range(random.randint(1, 3)):
            rand_airline = get_random(airlines)
            airline_string += f" {rand_airline},"
            completion_airline += f"AIRLINE: ['{rand_airline}']\n"

        completion_type = f"AIRLINE_INCL: ['{airline_type}']\n"
        return airline_string, completion_airline, completion_type
    return "", "", ""


def get_value():
    val = random.randint(3, 20)
    text_val = "millones"
    multiplier = 1000000
    if val < 10:
        multiplier = 1000
        val = val * 100
        text_val = "mil"
    if coin_flip():
        if coin_flip():
            return f" con un valor menor a {val*100000}", val * 100000
        return f" con un valor menor a {val} {text_val}", val * multiplier
    return "", ""


def days_range():
    range_texts = [
        "que dure z dias",
        "que no dure mas de z dias",
        "que tenga maxima duracion de z dias",
    ]
    rand = random.randint(1, 13)
    rand_string = random.choice(range_texts)
    completion = ""
    if coin_flip():
        string = rand_string.replace("z", str(rand))
        completion = f"DAYS: ['{str(rand)}']\n"
        return string, completion
    return "", ""


def get_date():
    rand = random.randint(0, len(dates) - 1)
    completion = ""
    formated_dates = []
    date_format = dates[rand]
    semanas = [
        ["primera", 1],
        ["segunda", 7],
        ["tercera", 14],
        ["cuarta", 21],
        ["ultima", 28],
    ]

    if rand == 0:
        first = random.randint(1, 29)
        last = random.randint(first, 31)
        month = get_random(months)

        formated_dates.append(f"{first} de {month}")
        formated_dates.append(f"{last} de {month}")

        date_format = date_format.replace("x", str(first))
        date_format = date_format.replace("k", str(last))
        date_format = date_format.replace("z", month)
    elif rand == 1:
        first = random.choice(semanas)
        last = random.choice(semanas)
        first_month = get_random(months)
        last_month = get_random(months)

        formated_dates.append(f"{first[1]} de {first_month}")
        formated_dates.append(f"{last[1]} de {last_month}")

        date_format = date_format.replace("x", first[0])
        date_format = date_format.replace("z", first_month)
        date_format = date_format.replace("k", last[0])
        date_format = date_format.replace("w", last_month)
    else:
        first_month = get_random(months)
        last_month = get_random(months)

        formated_dates.append(f"1 de {first_month}")
        formated_dates.append(f"28 de {last_month}")

        date_format = date_format.replace("z", first_month)
        date_format = date_format.replace("k", last_month)

    for date in formated_dates:
        completion += f"DATE: ['{date}']\n"

    return date_format, completion


def create_artificial_queries():
    queries = []
    temp_query = ""

    for n in range(400):
        destination = get_random(places)
        completion = ""
        ammenity, ammenity_comp = ran_ammenities()
        people_q, people_comp, more_info = get_random_people()
        if more_info == True:
            complete_people_q, complete_people_comp = complete_people()
        else:
            complete_people_q, complete_people_comp = "", ""
        airline_q, airline_comp, airline_incl_comp = get_airline_string()
        value, num_value = get_value()
        date, date_comp = get_date()
        event = get_random(events)
        final_destination = ""
        days_q, days_comp = days_range()
        evt = False
        if coin_flip():
            final_destination = f"{destination} {date}"
            temp_query = f"{get_random(verbs)} {final_destination} {people_q}{airline_q} {days_q} y {get_random(hosting_verb)} un airbnb {ammenity}{value}. {complete_people_q}\n\n###\n\n"
            completion = f"DESTINATION: ['{destination}']\n{airline_comp}{airline_incl_comp}{days_comp}VALUE: ['{num_value}']\n{date_comp}{people_comp}{complete_people_comp}{ammenity_comp}###"
        else:
            final_destination = event
            temp_query = f"{get_random(verbs)} {final_destination} {people_q}{airline_q} y {get_random(hosting_verb)} un airbnb {ammenity}{value}. {complete_people_q}\n\n###\n\n"
            completion = f"EVENT: ['{event}']\nAIRLINE: ['{airline_q}']\nVALUE: ['{num_value}']\n{people_comp}{complete_people_comp}{ammenity_comp}###"

        training_prompt = Prompt(temp_query, completion)
        queries.append(training_prompt)
    return queries


def create_training_patterns():
    types = ["EVENT", "PEOPLE", "PLACE", "MODIFIER", "AIRLINE", "MONTH", "AMMENITY"]
    patterns = []
    for data_type in types:
        pattern = extract_pattern(
            load_data(f"data/{data_type.lower()}.json"), data_type
        )
        for pat in pattern:
            patterns.append(pat)
            print(pat)
    return patterns


def extract_pattern(data, type):
    patterns = []

    for item in data:
        if type != "MODIFIER":
            item = item["value"]
        pattern = {"label": type, "pattern": item}
        patterns.append(pattern)
    return patterns


patterns = create_artificial_queries()
save_jsonl("training_gpt3.jsonl", patterns)
""" print(patterns) """
""" generate_rules(patterns) """
