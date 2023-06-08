import re
import dateparser
from utils import load_data, find_closest_object

people = load_data("data/people.json")
destinations = load_data("data/place.json")
events = load_data("data/event.json")
ammenity_list = load_data("data/ammenity.json")
airlines = load_data("data/airline.json")


def parse_dates(dates):
    parsed_dates = []
    for date in dates:
        parsed_dates.append(dateparser.parse(date).isoformat())
    return parsed_dates


entity_types = [
    "EVENT",
    "PEOPLE",
    "DATE",
    "VALUE",
    "AIRLINE",
    "AIRLINE_INCL",
    "DESTINATION",
    "AMMENITY",
    "DAYS",
    "ADULTS",
    "CHILDREN",
    "INFANTS",
]


def extract_type(completion):
    entities = {}
    print(completion)
    for ent_type in entity_types:
        regex_pattern = rf"{ent_type}:\s*\['(.*?)'\]"
        matches = re.findall(regex_pattern, completion)
        if matches:
            if ent_type == "DATE":
                entities[ent_type] = parse_dates(matches)
            elif ent_type in ["AMMENITY", "AIRLINE"]:
                entities[ent_type] = matches
            else:
                entities[ent_type] = matches[0]

    return translate_object(entities)


def ent_from_data(entities, ent_type):
    ent = entities.get(ent_type)
    print(ent)
    if ent:
        match ent_type:
            case "PEOPLE":
                return {"adults": find_closest_object(ent, people, "value")["amount"]}
            case "DATE":
                return {
                    "startDate": ent[0],
                    "endDate": ent[1],
                }
            case "DESTINATION":
                matched = find_closest_object(ent, destinations, "value")
                return {
                    "destination": {"IATA": matched["key"], "name": matched["value"]},
                    "origin": {"IATA": "CLO", "name": "Cali"},
                }
            case "DAYS":
                return {"duration": int(ent)}
            case "VALUE":
                return {"maxPrice": ent}
            case "EVENT":
                matched = find_closest_object(ent, events, "value")
                return {"destination": matched["key"], "origin": "CLO"}
            case "AMMENITY":
                ammenities = []
                for am in ent:
                    ammenities.append(find_closest_object(am, ammenity_list, "value"))
                keys = [item["key"] for item in ammenities]
                return {"features": keys}
            case "AIRLINE":
                airlines_list = []
                for air in ent:
                    airlines_list.append(find_closest_object(air, airlines, "value"))
                return {"airlines": airlines_list}
            case "AIRLINE_INCL":
                return {"airline_incl": ent}
            case "ADULTS":
                return {"adults": ent}
            case "CHILDREN":
                return {"children": ent}
            case "INFANTS":
                return {"infants": ent}
            case _:
                return {}


def translate_object(obj):
    translated_obj = dict()
    airline_incl = ""
    airline_list = []

    for ent_type in entity_types:
        temp = ent_from_data(obj, ent_type)
        print(temp)
        if ent_type == "AIRLINE":
            airline_list = temp
            continue
        elif ent_type == "AIRLINE_INCL":
            airline_incl = temp
            continue
        elif airline_incl and airline_list:
            translated_obj.update(airlines_list(airline_list, airline_incl))
        if temp:
            translated_obj.update(temp)

    return translated_obj


def airlines_list(air_list, incl):
    all_airlines = [0, 1, 2, 3, 4, 5, 6, 7]
    key_values = [item["key"] for item in air_list["airlines"]]

    if incl == "include":
        return {"allowAerolines": key_values}
    else:
        return {
            "allowAerolines": [
                element for element in all_airlines if element not in key_values
            ]
        }


"""     for ent_type in entity_types: """


# Minimum object
""" {
    adults: '1',
    origin: origin,
    destination: destination,
    startDate: startDate,
    endDate: endDate,
    location: 'Medellin',
    checkin: checkin,   
    checkout: checkout,
    adults: '1',
    children: '0',
} """
