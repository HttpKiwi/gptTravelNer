import re
from src.utils import load_data, find_closest_object
from src.entity_utils import parse_dates, convert


people = load_data("data/people.json")
destinations = load_data("data/place.json")
events = load_data("data/event.json")
ammenity_list = load_data("data/ammenity.json")
airlines = load_data("data/airline.json")

entity_types = [
    "EVENT",
    "PERSON",
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
    "ORIGIN",
    "BEDS",
    "BATHROOMS",
    "ROOMS"
]

temporal_duration = 0


def extract_type(completion):
    entities = {}
    for ent_type in entity_types:
        regex_pattern = rf"{ent_type}:\s*\['(.*?)'\]"
        matches = re.findall(regex_pattern, completion)
        if matches:
            if ent_type == "DATE":
                entities[ent_type], dates = parse_dates(matches)
                global temporal_duration
                temporal_duration = abs((dates[0] - dates[1]).days) + 1
            elif ent_type in ["AMMENITY", "AIRLINE", "PERSON"]:
                entities[ent_type] = matches
            else:
                entities[ent_type] = matches[0]
    return translate_object(entities)


def ent_from_data(entities, ent_type):
    ent = entities.get(ent_type)
    if ent:
        match ent_type:
            case "PERSON":
                total_adults = 0
                for person in ent:
                    temp = find_closest_object(person, people, "value")["amount"]
                    if temp == -1:
                        return {"adults": -1}
                    total_adults += temp
                return {"adults": total_adults - len(ent) + 1}
            case "DATE":
                return {
                    "startDate": ent[0],
                    "endDate": ent[1],
                }
            case "DESTINATION":
                matched = find_closest_object(ent, destinations, "value")
                return {
                    "destination": {"IATA": matched["key"], "name": matched["value"]}
                }
            case "ORIGIN":
                matched = find_closest_object(ent, destinations, "value")
                return {"origin": {"IATA": matched["key"], "name": matched["value"]}}
            case "DAYS":
                return {"duration": int(ent)}
            case "VALUE":
                return {"maxPrice": convert(int(ent))}
            case "EVENT":
                matched = find_closest_object(ent, events, "value")
                global temporal_duration
                dates_iso, dates_parse = parse_dates(
                    [matched["startDate"], matched["endDate"]]
                )
                temporal_duration = abs(
                    (dates_parse[0] - dates_parse[1]).days
                ) + 1
                print(dates_iso)
                return {
                    "destination": {
                        "IATA": matched["key"],
                        "name": matched["location"],
                    },
                    "startDate": dates_iso[0],
                    "endDate": dates_iso[1],
                    "duration": temporal_duration,
                }
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
            case "BEDS":
                return {"beds": ent}
            case "ROOMS":
                return {"rooms": ent}
            case "BATHROOMS":
                return {"bathrooms": ent}
            
            case _:
                return {}


def translate_object(obj):
    translated_obj = dict()
    airline_incl = "include"
    airline_list = []

    for ent_type in entity_types:
        temp = ent_from_data(obj, ent_type)
        if ent_type == "AIRLINE":
            airline_list = temp
            continue
        elif ent_type == "AIRLINE_INCL":
            airline_incl = temp if temp else "include"

            continue
        elif airline_incl and airline_list:
            translated_obj.update(airlines_list(airline_list, airline_incl))
        elif ent_type == "DAYS" and temp == None:
            if temporal_duration == 0:
                temp = {}
            else:
                temp = {"duration": temporal_duration}

        if temp:
            translated_obj.update(temp)

    return translated_obj


def airlines_list(air_list, incl):
    all_airlines = [0, 1, 2, 3, 4, 5, 6, 7]
    key_values = [item["key"] for item in air_list["airlines"]]

    if incl["airline_incl"] == "include":
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
