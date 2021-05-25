import os.path
import sys

import pandas as pd

from tqdm import tqdm


def main(anual_flights_dir:str,weather_dir:str,out_dir:str, carrier:str, origin_airport:str,destination_airport:str, start_time:int, end_time:int):
    flight_data_per_year = []
    try:
        # For each file in the directory
        # Get CSV Files and create a pandas dataframe for each annual data
        flights_directory = os.path.join(anual_flights_dir)
        for root, dirs, files in tqdm(os.walk(flights_directory)):
            for file in tqdm(files):
                if file.endswith(".csv"):
                    with open(f"{flights_directory}/{file}", "r") as f:
                        df = pd.read_csv(f)
                    flight_data_per_year.append(df)
    except Exception as e:
        raise e#ValueError(f"The file path {flights_directory} does not exists")

    for dataframe in tqdm(flight_data_per_year):
        filtered_dataframe = dataframe.loc[(dataframe['CRS_DEP_TIME'] >= int(start_time)) & (dataframe['CRS_DEP_TIME'] <= int(end_time))]
        filtered_dataframe = filtered_dataframe.loc[filtered_dataframe['OP_CARRIER'] == carrier]
        filtered_dataframe = filtered_dataframe.loc[filtered_dataframe['ORIGIN'] == origin_airport]
        filtered_dataframe = filtered_dataframe.loc[filtered_dataframe['DEST'] == destination_airport]
        year = filtered_dataframe.loc[1,'FL_DATE'][0:3]
        filtered_dataframe.to_csv(f"{out_dir}/{year}_{carrier}_{origin_airport}_{destination_airport}_{start_time}_{end_time}.csv")

    weather_directory = os.path.join(weather_dir)
    for root, dirs, files in tqdm(os.walk(weather_directory)):
        for file in tqdm(files):
            if file.startswith(origin_airport):
                with open(f"{weather_directory + file}", "r") as f:
                    df = pd.read_csv(f)
                    df['Year'] = df['hour'].str.split('-',expand=True)[0]
                    group_df = df.groupby['Year']
                    for group in group_df.groups:
                        annual_df = group_df.get_group(group)
                        annual_df.to_csv(f"{out_dir}/{group}_{origin_airport}.csv")
            elif file.startswith(destination_airport):
                df = pd.read_csv(f)
                df['Year'] = df['hour'].str.split('-', expand=True)[0]
                group_df = df.groupby['Year']
                for group in group_df.groups:
                    annual_df = group_df.get_group(group)
                    annual_df.to_csv(f"{out_dir}/{group}_{destination_airport}.csv")

if __name__ == '__main__':
    if len(sys.argv[1:]) != 8:
        print("There are some parameters of the function are missing.")
        print((sys.argv[1:]))
        exit(1)
    main(*sys.argv[1:])