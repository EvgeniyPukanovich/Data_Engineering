import json


def insert_data(filename, data):
    with open(filename, "w") as r_json:
        r_json.write(
            json.dumps(
                data,
                indent=2,
                ensure_ascii=False,
            )
        )
