import os.path
import sys

import pandas as pd

from tqdm import tqdm


def main(anual_flights_dir:str,weather_dir:str,out_dir:str, carrier:str, origin_airport:str,destination_airport:str, start_time:int, end_time:int):
    """
    Function that split data per according to query

    :param anual_flights_dir: Directory containing all the departures per year
    :param weather_dir: Directory containing the meteorological data each day for each airport
    :param out_dir: Output directory
    :param carrier: Carrier of the departure
    :param origin_airport: Airport of origin
    :param destination_airport: Airport of destination
    :param start_time: Lower bound for scheduled departure time
    :param end_time: Upper bound for scheduled departure time
    """

    flight_data_per_year = []
    try:
        # For each file in the directory containing departures data
        # Get CSV Files and create a pandas dataframe for each annual data
        flights_directory = os.path.join(anual_flights_dir)
        for root, dirs, files in tqdm(os.walk(flights_directory)):
            for file in tqdm(files):
                if file.endswith(".csv"):
                    with open(f"{flights_directory}/{file}", "r") as f:
                        df = pd.read_csv(f)
                    flight_data_per_year.append(df)
    except Exception as e:
        raise e

    # For each dataframe containing departures information
    # Perform the desired query and store its results in a csv file
    for dataframe in tqdm(flight_data_per_year):
        # Filter by scheduled departure time range
        filtered_dataframe = dataframe.loc[(dataframe['CRS_DEP_TIME'] >= int(start_time)) & (dataframe['CRS_DEP_TIME'] <= int(end_time))]
        # Filter by carrier
        filtered_dataframe = filtered_dataframe.loc[filtered_dataframe['OP_CARRIER'] == carrier]
        # Filter by airport of origin
        filtered_dataframe = filtered_dataframe.loc[filtered_dataframe['ORIGIN'] == origin_airport]
        # Filter by airport of destination
        filtered_dataframe = filtered_dataframe.loc[filtered_dataframe['DEST'] == destination_airport]
        # Extract the year of the data
        year = filtered_dataframe.iloc[1,0].split('-')[0]
        # Save CSV File
        filtered_dataframe.to_csv(f"{out_dir}/Flights/{year}_{carrier}_{origin_airport}_{destination_airport}_{start_time}_{end_time}.csv",index=False)
        print(
            f"File saved: {out_dir}/Flights/{year}_{carrier}_{origin_airport}_{destination_airport}_{start_time}_{end_time}.csv")

    # For each file in the directory containing meteorological data
    # We select those containing the information about the airport of
    # origin or destination
    weather_directory = os.path.join(weather_dir)
    for root, dirs, files in tqdm(os.walk(weather_directory)):
        for file in tqdm(files):
            if file.startswith(origin_airport):
                with open(f"{weather_directory}/{file}", "r") as f:
                    # Create dataframe
                    df = pd.read_csv(f)

                # Add a new column to add the year information
                df['Year'] = df['hour'].str.split('-',expand=True)[0]

                # Grouping by year and save CSV File for the data per year
                group_df = df.groupby(['Year'])
                for group in group_df.groups:
                    annual_df = group_df.get_group(group)
                    annual_df.to_csv(f"{out_dir}/Meteo/{group}_{origin_airport}.csv",index=False)
                    print(f"File saved: {out_dir}/Meteo/{group}_{origin_airport}.csv")

            elif file.startswith(destination_airport):
                with open(f"{weather_directory}/{file}", "r") as f:
                    # Create dataframe
                    df = pd.read_csv(f)

                # Add a new column to add the year information
                df['Year'] = df['hour'].str.split('-', expand=True)[0]
                group_df = df.groupby(['Year'])

                # Grouping by year and save CSV File for the data per year
                for group in group_df.groups:
                    annual_df = group_df.get_group(group)
                    annual_df.to_csv(f"{out_dir}/{group}_{destination_airport}.csv", index=False)
                    print(f"File saved: {out_dir}/Meteo/{group}_{destination_airport}.csv")

if __name__ == '__main__':
    if len(sys.argv[1:]) != 8:
        print("There are some parameters of the function are missing.")
        print((sys.argv[1:]))
        exit(1)
    main(*sys.argv[1:])