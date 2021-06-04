import os.path
import sys

import pandas as pd

from tqdm import tqdm


def main(flight_data_file, meteo_data_file, out_dir):

    with open(flight_data_file, 'r') as f:
        f_full_name = f.name
        flights_name = os.path.basename(f_full_name)

    with open(meteo_data_file, 'r') as f:
        f_full_name = f.name
        meteo_name = os.path.basename(f_full_name)

    flight_dataframe = pd.read_csv(flight_data_file)

    flight_dataframe['Month'] = flight_dataframe['FL_DATE'].str.split('-', expand=True)[1]

    monthly_group_df = flight_dataframe.groupby(['Month'])

    for month in monthly_group_df.groups:
        monthly_df = monthly_group_df.get_group(month)
        monthly_df.to_csv(f"{out_dir}/Flights/{month}_{flights_name}")
        print(f"File saved: {month}_{flights_name}")

    meteo_dataframe = pd.read_csv(meteo_data_file)

    meteo_dataframe['Month'] = meteo_dataframe['hour'].str.split('-', expand=True)[1]

    monthly_group_df = meteo_dataframe.groupby(['Month'])

    for month in monthly_group_df.groups:
        monthly_df = monthly_group_df.get_group(month)
        monthly_df.to_csv(f"{out_dir}/Meteo/{month}_{meteo_name}")
        print(f"File saved: {month}_{meteo_name}")


if __name__ == '__main__':
    if len(sys.argv[1:]) != 3:
        print("There are some parameters of the function are missing.")
        print((sys.argv[1:]))
        exit(1)
    main(*sys.argv[1:])