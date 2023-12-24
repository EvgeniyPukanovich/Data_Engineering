import pandas as pd
import matplotlib
import numpy as np
import os
from typing import Type
import json


pd.set_option("display.max_rows", 20, "display.max_columns", 60)  # type: ignore


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


def insert_data(filename, data):
    with open(filename, "w", encoding="utf-8") as r_json:
        json.dump(data, r_json, indent=2, ensure_ascii=False)


def get_memory_stats(df: pd.DataFrame, file_name: str):
    file_size = {"file_size_KB": os.path.getsize(file_name) // 1024}

    memory_usage_stat = df.memory_usage(deep=True)
    total_memory_usage = memory_usage_stat.sum()
    in_memory_size = {"file_in_memory_size_KB": total_memory_usage // 1024}

    column_stat = pd.DataFrame(
        {
            "column_name": df.columns,
            "memory_abs": [memory_usage_stat[key] // 1024 for key in df.columns],
            "memory_per": [
                round(memory_usage_stat[key] / total_memory_usage * 100, 4)
                for key in df.columns
            ],
            "dtype": df.dtypes.values,
        }
    )

    column_stat_sorted = column_stat.sort_values(by="memory_abs", ascending=False)
    return (file_size, in_memory_size, column_stat_sorted)


def change_obj_to_cat(df: pd.DataFrame):
    for column in df.columns:
        if df[column].dtype == "object":
            unique_values = len(df[column].unique())
            total_values = len(df[column])
            if unique_values / total_values < 0.5:
                df[column] = df[column].astype("category")
        if pd.api.types.is_integer_dtype(df[column]):
            df[column] = pd.to_numeric(df[column], downcast="unsigned")
        if pd.api.types.is_float_dtype(df[column]):
            df[column] = pd.to_numeric(df[column], downcast="float")


def print_memory_stats(file_stat: dict[str, int], mem_stat: dict, by_columns: pd.DataFrame, output_file_name: str):

    with open(output_file_name, "w", encoding="utf-8") as r_json:
        combined_json = {}
        combined_json.update(file_stat)
        combined_json.update(mem_stat)
        res = by_columns.to_json(orient="index", default_handler=str)
        parsed = json.loads(res)
        combined_json.update(parsed)
        json.dump(combined_json, r_json, indent=2, ensure_ascii=False, cls=NpEncoder)