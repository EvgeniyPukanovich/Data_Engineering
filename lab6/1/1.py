import pandas as pd
import matplotlib
from typing import Type
import sys

sys.path.append("..")
from utils import print_memory_stats, change_obj_to_cat, NpEncoder

file_name = "game_logs.csv"
column_types_path = "column_types.pkl"
ten_columns_path = "10_columns.csv"


def change_types(my_df: pd.DataFrame):
    print_memory_stats(my_df, file_name, "mem_res_no_opt.json")
    print("before:")
    print(my_df.info(memory_usage="deep"))
    change_obj_to_cat(my_df)
    print_memory_stats(my_df, file_name, "mem_res_opt.json")
    print("after:")
    print(my_df.info(memory_usage="deep"))


def save_10_columns(my_df: pd.DataFrame):
    column_names = [
        "date",
        "number_of_game",
        "day_of_week",
        "park_id",
        "v_manager_name",
        "length_minutes",
        "v_hits",
        "h_hits",
        "h_walks",
        "h_errors",
    ]
    types = my_df.dtypes.to_dict()
    first_chunk = True
    for chunk in pd.read_csv(
        file_name,
        usecols=lambda x: x in column_names,
        dtype=types,
        chunksize=100_000,
    ):
        chunk.to_csv(ten_columns_path, mode= 'w' if first_chunk else 'a', header=first_chunk, index=False)
        first_chunk = False

    with open(column_types_path, "wb") as file:
        pd.to_pickle(types, file)


my_df = pd.read_csv(file_name)
change_types(my_df)
save_10_columns(my_df)

with open(column_types_path, "rb") as file:
    loaded_column_types = pd.read_pickle(file)
for k, v in loaded_column_types.items():
    print(k, v)
df = pd.read_csv(ten_columns_path, dtype=loaded_column_types)
print(df.info(memory_usage="deep"))

#     # df = pd.read_csv(datasets [year], chunksize=chunksize, compression='gzip')
