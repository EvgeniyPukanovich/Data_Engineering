import csv
from dataclasses import dataclass
import os
import sys
import math
from typing import Callable
import json
import msgpack
import pickle


@dataclass
class DataHolder:
    city: str
    state: str
    model_year: int
    make: str
    model: str
    ev_type: str
    e_range: int
    msrp: int


filename = "Electric_Vehicle_Population_Data.csv"


def getInt(number: str) -> int:
    return int(number) if number else 0


with open(filename, newline="\n", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    vehicles = list(
        map(
            lambda x: DataHolder(
                x["City"],
                x["State"],
                getInt(x["Model Year"]),
                x["Make"],
                x["Model"],
                x["Electric Vehicle Type"],
                getInt(x["Electric Range"]),
                getInt(x["Base MSRP"]),
            ),
            reader,
        )
    )


city_dict: dict[str, int] = dict()
state_dict = dict()
model_year_max = 0
model_year_min = sys.maxsize
model_year_non_empty = 0
model_year_sum = 0
make_dict = dict()
model_dict = dict()
ev_type_dict = dict()
e_range_max = 0
e_range_min = sys.maxsize
e_range_non_empty = 0
e_range_sum = 0
msrp_max = 0
msrp_min = sys.maxsize
msrp_non_empty = 0
msrp_sum = 0


def handle_int_value(value: int, max: int, min: int, non_empty: int, sum: int):
    if value != 0:
        non_empty += 1
        sum += value
        if value > max:
            max = value
        if value < min:
            min = value
    return max, min, non_empty, sum


def handle_string_value(value: str, dict: dict):
    if value != "":
        dict[value] = dict.get(value, 0) + 1
    return dict


for vehicle in vehicles:
    city_dict = handle_string_value(vehicle.city, city_dict)
    state_dict = handle_string_value(vehicle.state, state_dict)
    make_dict = handle_string_value(vehicle.make, make_dict)
    model_dict = handle_string_value(vehicle.model, model_dict)
    ev_type_dict = handle_string_value(vehicle.ev_type, ev_type_dict)

    (
        model_year_max,
        model_year_min,
        model_year_non_empty,
        model_year_sum,
    ) = handle_int_value(
        vehicle.model_year,
        model_year_max,
        model_year_min,
        model_year_non_empty,
        model_year_sum,
    )
    e_range_max, e_range_min, e_range_non_empty, e_range_sum = handle_int_value(
        vehicle.e_range, e_range_max, e_range_min, e_range_non_empty, e_range_sum
    )
    msrp_max, msrp_min, msrp_non_empty, msrp_sum = handle_int_value(
        vehicle.msrp, msrp_max, msrp_min, msrp_non_empty, msrp_sum
    )


def get_std_dev(avr: float, get_field: Callable[[DataHolder], int]) -> float:
    sum = 0
    for vehicle in vehicles:
        field = get_field(vehicle)
        if field != 0:
            sum += (get_field(vehicle) - avr) ** 2
    return math.sqrt(sum / (len(vehicles) - 1))


model_year_avr = model_year_sum / model_year_non_empty
model_year_dev = get_std_dev(model_year_avr, lambda x: x.model_year)

e_range_avr = e_range_sum / e_range_non_empty
e_range_dev = get_std_dev(e_range_avr, lambda x: x.e_range)

msrp_avr = msrp_sum / msrp_non_empty
msrp_dev = get_std_dev(msrp_avr, lambda x: x.msrp)

result = {
    "city_freq": dict(
        sorted(city_dict.items(), reverse=True, key=lambda item: item[1])
    ),
    "state_freq": dict(
        sorted(state_dict.items(), reverse=True, key=lambda item: item[1])
    ),
    "make_freq": dict(
        sorted(make_dict.items(), reverse=True, key=lambda item: item[1])
    ),
    "model_freq": dict(
        sorted(model_dict.items(), reverse=True, key=lambda item: item[1])
    ),
    "ev_type_freq": dict(
        sorted(ev_type_dict.items(), reverse=True, key=lambda item: item[1])
    ),
    "model_year_stat": {
        "max": model_year_max,
        "min": model_year_min,
        "avr": model_year_avr,
        "sum": model_year_sum,
        "dev": model_year_dev,
    },
    "e_range_stat": {
        "max": e_range_max,
        "min": e_range_min,
        "avr": e_range_avr,
        "sum": e_range_sum,
        "dev": e_range_dev,
    },
    "msrp_stat": {
        "max": msrp_max,
        "min": msrp_min,
        "avr": msrp_avr,
        "sum": msrp_sum,
        "dev": msrp_dev,
    },
}


with open("result.json", "w") as r_json:
    r_json.write(json.dumps(result))


with open(filename, newline="\n", encoding="utf-8") as file:
    reader = csv.reader(file)
    res = list(map(lambda x: list(x), reader))

    with open("copy.json", "w") as r_json:
        r_json.write(json.dumps(res))

    with open("copy.msgpack", "wb") as r_msgpack:
        r_msgpack.write(msgpack.dumps(res)) # type: ignore

    with open("copy.pkl", "wb") as f:
        f.write(pickle.dumps(res))

    print(f"json    = {os.path.getsize('copy.json')}")
    print(f"msgpack = {os.path.getsize('copy.msgpack')}")
    print(f"pickle  = {os.path.getsize('copy.pkl')}")
