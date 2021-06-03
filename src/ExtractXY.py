import csv
import os
import sys

import numpy as np
import pandas as pd

from tqdm import tqdm


def main(flights_dir, weather_dir, out_dir, carrier, origin, destination, start_time, end_time, n1=20,n2=5,n3=10,n4=15):
    """
    Create an Matrix file containing the XY by adding extra information to the data about carrier and ariports of
    origin and destination.

    :param flights_dir: Directory where the flight data is contained
    :param weather_dir: Directory where the meteorological data is contained
    :param out_dir: Directory to save the file
    :param carrier: Carrier of the target task
    :param origin: Airport of origin of the target task
    :param destination: Airport of destination of the target task
    :param start_time: Lower bound for departure time
    :param end_time: Upper bound for departure time
    :param n1: Number of recents flights at the same origin. Default to 20.
    :param n2: Number of recents flights by the same carrier at the same origin. Default to 5.
    :param n3: Number of recents flights by the same carrier. Default to 10.
    :param n4: Number of recents flights at the same destination. Default to 15.
    """

    # Dataframe to store the prediction data
    prediction_dataframe = pd.DataFrame(
        columns=['FL_DATE', 'OP_CARRIER_FL_NUM', 'OP_CARRIER', 'CRS_DEP_TIME', 'DEP_DELAY','CANCELLED'])

    # Dataframe to store the weather information at the airport of origin
    weather_at_origin_dataframe = pd.DataFrame(columns=['hour', 'temperature', 'dewPoint', 'visibility',
                                               'humidity', 'cloudCover', 'pressure', 'windSpeed', 'windBearing', 'precipType', 'icon', 'summary'])

    # Dataframe to store the weather information at the airport of destination
    weather_at_destination_dataframe = pd.DataFrame(columns=['hour', 'temperature', 'dewPoint', 'visibility',
                                                             'humidity', 'cloudCover', 'pressure', 'windSpeed', 'windBearing', 'precipType', 'icon', 'summary'])

    # Dataframe to store information about recent flights from the airport of origin and within the same departure time range
    recents_at_origin = pd.DataFrame(
        columns=['FL_DATE', 'OP_CARRIER_FL_NUM', 'CANCELLED', 'CRS_DEP_TIME', 'DEP_DELAY'])

    # Dataframe to store information about the recent flights from the airport of origin and within the same departure time range by the same carrier
    carrier_recents_at_origin = pd.DataFrame(
        columns=['FL_DATE', 'OP_CARRIER_FL_NUM', 'CANCELLED', 'CRS_DEP_TIME', 'DEP_DELAY'])

    # Dataframe to store information about the recent flights from the same carrier at the same time range
    carrier_recents = pd.DataFrame(
        columns=['FL_DATE', 'OP_CARRIER_FL_NUM', 'CANCELLED', 'CRS_DEP_TIME', 'DEP_DELAY'])

    # Dataframe to store information about recent flights at the same airport of destination
    recents_at_destination = pd.DataFrame(
        columns=['FL_DATE', 'OP_CARRIER_FL_NUM', 'CANCELLED', 'CRS_DEP_TIME', 'DEP_DELAY'])

    try:
        # For each file in the directory containing departures data
        # Get CSV Files and create a pandas dataframe for each annual data
        flights_directory = os.path.join(flights_dir)
        for root, dirs, files in tqdm(os.walk(flights_directory)):
            for file in tqdm(files):
                if file.endswith(".csv"):
                    with open(f"{flights_directory}/{file}", "r") as f:
                        dataframe = pd.read_csv(f)
                        # Filter by the departure time range
                        time_filtered = dataframe.loc[(dataframe['CRS_DEP_TIME'] >= int(
                            start_time)) & (dataframe['CRS_DEP_TIME'] <= int(end_time))]

                        #======== Add extra information about the airport of origin =======#

                        # Filter by the airport of origin and add this information to the dataframe for the recent flights at the origin
                        origin_filtered = time_filtered.loc[(
                            time_filtered['ORIGIN'] == origin)]
                        # Sort by values and take the N1 most recent
                        origin_filtered = origin_filtered.sort_values(by=['FL_DATE','CRS_DEP_TIME'],ascending=True)
                        recents_at_origin = recents_at_origin.append(origin_filtered[[
                                                 'FL_DATE', 'OP_CARRIER_FL_NUM', 'CANCELLED', 'CRS_DEP_TIME', 'DEP_DELAY','OP_CARRIER']])

                        # Filter by carrier and add this information to the dataframe for the recent flights at the origin by the same carrier
                        carrier_origin_filtered = origin_filtered.loc[(
                            origin_filtered['OP_CARRIER']) == carrier]
                        # Sort by values and take the N2 most recent
                        carrier_origin_filtered = carrier_origin_filtered.sort_values(by=['FL_DATE','CRS_DEP_TIME'],ascending=True)

                        recents_by_carrier_at_origin = carrier_recents_at_origin.append(carrier_origin_filtered[[
                                                         'FL_DATE', 'OP_CARRIER_FL_NUM', 'CANCELLED', 'CRS_DEP_TIME', 'DEP_DELAY']])

                        # ======== Add extra information about the carrier =======#

                        # Filter by the carrier at the airport of origin and add this information to the dataframe for the recent flights
                        # at origin by the same carrier
                        carrier_filtered = origin_filtered.loc[(
                                                                   time_filtered['OP_CARRIER']) == carrier]
                        # Sort by values and take the N3 most recent
                        carrier_filtered = carrier_filtered.sort_values(by=['FL_DATE','CRS_DEP_TIME'],ascending=True)
                        recents_by_carrier = carrier_recents.append(carrier_filtered[[
                            'FL_DATE', 'OP_CARRIER_FL_NUM', 'CANCELLED', 'CRS_DEP_TIME', 'DEP_DELAY']]).iloc[:n3]

                        #======== Add extra information about the airport of destination =======#

                        # Filter by the airport of destination and add this information to the dataframe for the recent flights at the destination
                        destination_filtered = time_filtered.loc[(
                            time_filtered['DEST'] == destination)]
                        # Sort by values and take the N4 most recent
                        destination_filtered = destination_filtered.sort_values(by=['FL_DATE','CRS_DEP_TIME'],ascending=True)
                        recents_at_destination = recents_at_destination.append(destination_filtered[[
                                                 'FL_DATE', 'OP_CARRIER_FL_NUM', 'CANCELLED', 'CRS_DEP_TIME', 'DEP_DELAY']])


                        # Extract information about the target entailment

                        # For the prediction task, we filtered the flights by the given origin and destination airport, by the specific
                        # carrier within the departure time range and add this information to the dataframe
                        prediction_filtered = carrier_filtered.loc[(carrier_origin_filtered['DEST'] == destination)]
                        prediction_dataframe = prediction_dataframe.append(
                            prediction_filtered[['FL_DATE', 'OP_CARRIER_FL_NUM', 'OP_CARRIER', 'CRS_DEP_TIME', 'DEP_DELAY','CANCELLED']])

        weather_directory = os.path.join(weather_dir)
        for root, dirs, files in tqdm(os.walk(weather_directory)):
            for file in tqdm(files):
                # Get the meteorological data of the airport of origin
                if file.startswith(origin):
                    with open(f"{weather_directory}/{file}", "r") as f:
                        # Create dataframe for origin
                        weather_at_origin_dataframe = pd.read_csv(
                            f)
                        # Split the column hour (YY-MM-DDTHH format) to extract the date and the time of the weather
                        weather_at_origin_dataframe['DATE'] = weather_at_origin_dataframe['hour'].str.split(r'T',expand=True)[0]
                        weather_at_origin_dataframe['DATE_TIME'] = weather_at_origin_dataframe['hour'].str.split(r'T',expand=True)[1]
                        # Get the weather according the time frame
                        weather_at_origin_dataframe = weather_at_origin_dataframe.loc[(weather_at_origin_dataframe['DATE_TIME'] == start_time[:2])]
                        # Drop hour (unnecessary)
                        weather_at_origin_dataframe = weather_at_origin_dataframe.drop('hour',axis=1)

                # Get the meteorological data of the airport of destination
                elif file.startswith(destination):
                    with open(f"{weather_directory}/{file}", "r") as f:
                        # Create dataframe for destination
                        weather_at_destination_dataframe = pd.read_csv(
                            f)
                        # Split the column hour (YY-MM-DDTHH format) to extract the date and the time of the weather
                        weather_at_destination_dataframe['DATE'] = \
                        weather_at_destination_dataframe['hour'].str.split(r'T', expand=True)[0]
                        weather_at_destination_dataframe['DATE_TIME'] = \
                        weather_at_destination_dataframe['hour'].str.split(r'T', expand=True)[1]
                        # Get the weather according the time frame
                        weather_at_destination_dataframe = weather_at_destination_dataframe.loc[
                            (weather_at_destination_dataframe['DATE_TIME'] == start_time[:2])]
                        # Drop hour (unnecessary)
                        weather_at_destination_dataframe = weather_at_destination_dataframe.drop('hour', axis=1)




    except Exception as e:
        raise e

    # Now that we have extract and filtered all the information needed we need to combine the data to
    # obtain the X and Y matrices we are going to used to train our model. First of all we are going to
    # combine this information in a pandas dataframe

    # First we are going to the set features of  interesrt for XY dataframe
    # Meteo feature columns
    meteo_features = ['temperature', 'dewPoint', 'visibility', 'humidity','cloudCover', 'pressure','windSpeed','windBearing']
    origin_meteo_features = [f'{feature}_ORIGIN' for feature in meteo_features]
    dest_meteo_features = [f'{feature}_DEST' for feature in meteo_features]

    # Departures delays feature columns for the different
    delays_features = ['DEP_DELAY']
    origin_features = [f'{feature}_ORIGIN_{num}' for feature in delays_features for num in range(1,n1+1)]
    carrier_features = [f'{feature}_CARRIER_{num}' for feature in delays_features for num in range(1, n2 + 1)]
    carrier_origin_features = [f'{feature}_CARRIER_ORIGIN_{num}' for feature in delays_features for num in range(1, n3 + 1)]
    dest_features = [f'{feature}_DEST_{num}' for feature in delays_features for num in range(1, n4 + 1)]

    matrix_dataframe = pd.DataFrame(columns=['FL_DATE','CANCELLED'] + origin_meteo_features + origin_features + carrier_features + carrier_origin_features
                                            + dest_features + dest_meteo_features)



    # Match the flight date and the cancellation label of each flight in the target
    matrix_dataframe[['FL_DATE','CANCELLED']] = prediction_dataframe.loc[:,['FL_DATE','CANCELLED']]
    # Set the day as index
    matrix_dataframe = matrix_dataframe.set_index('FL_DATE')

    # ======== Add meteorological data in the airport of origin =======#
    # Iterate through each flight date
    for date, row in tqdm(matrix_dataframe.iterrows()):
            # Extract the weather information of that date and convert it to a dictionary
            weather_filtered = weather_at_origin_dataframe.loc[(weather_at_origin_dataframe['DATE'] == date)]
            weather_dict = weather_filtered.to_dict('list')
            # Update each feature in the XY dataframe
            for feature in meteo_features:
                matrix_dataframe.loc[date,f"{feature}_ORIGIN"] = weather_dict[feature][0]

    # ======== Add meteorological data in the airport of destination =======#
    # Iterate through each flight date
    for date, row in tqdm(matrix_dataframe.iterrows()):
            # Extract the weather information of that date and convert it to a dictionary
            weather_filtered_dest = weather_at_destination_dataframe.loc[(weather_at_destination_dataframe['DATE'] == date)]
            weather_dict = weather_filtered_dest.to_dict('list')
            # Update each feature in the XY dataframe
            for feature in meteo_features:
                matrix_dataframe.loc[date,f"{feature}_DEST"] = weather_dict[feature][0]

    # ======== Add data about recent flights in the airport of origin =======#

    delay_idx = recents_at_origin.columns.get_loc('DEP_DELAY')
    for i in range(n1):
        # Iterate through each flight date and the corresponding value to the XY datafram
        for date, row in tqdm(matrix_dataframe.iterrows()):
            filtered_or = recents_at_origin.loc[(recents_at_origin['FL_DATE'] == date)]
            values = filtered_or['DEP_DELAY'].values
            for ft_idx in range(len(origin_features)):
                matrix_dataframe.loc[date, f"{origin_features[ft_idx]}"] = values[ft_idx]

    # ======== Add data about recent flights in the airport of origin  by same carrier =======#

    delay_idx = recents_by_carrier_at_origin.columns.get_loc('DEP_DELAY')
    for i in range(n2):
        # Iterate through each flight date and the corresponding value to the XY datafram
        for date, row in tqdm(matrix_dataframe.iterrows()):
            filtered_or = recents_by_carrier_at_origin.loc[(recents_by_carrier_at_origin['FL_DATE'] == date)]
            values = filtered_or['DEP_DELAY'].values
            for ft_idx in range(len(carrier_origin_features)):
                matrix_dataframe.loc[date, f"{carrier_origin_features[ft_idx]}"] = values[ft_idx]

    # ======== Add data about recent flights by same carrier =======#

    delay_idx = recents_by_carrier.columns.get_loc('DEP_DELAY')
    for i in range(n3):
        # Iterate through each flight date and the corresponding value to the XY dataframe
        # If values not present set 1400
        for date, row in tqdm(matrix_dataframe.iterrows()):
            filtered_or = recents_by_carrier.loc[(recents_by_carrier['FL_DATE'] == date)]
            values = filtered_or['DEP_DELAY'].values
            if len(filtered_or.dropna()) > 0:
                for ft_idx in range(len(carrier_features)):
                    matrix_dataframe.loc[date, f"{carrier_features[ft_idx]}"] = values[ft_idx]
            else:
                for ft_idx in range(len(carrier_features)):
                    matrix_dataframe.loc[date, f"{carrier_features[ft_idx]}"] =1440

    # ======== Add data about recent flights in the airport of destination =======#

    delay_idx = recents_at_destination.columns.get_loc('DEP_DELAY')
    for i in range(n3):
        # Iterate through each flight date and the corresponding value to the XY datafram
        for date, row in tqdm(matrix_dataframe.iterrows()):
            filtered_or = recents_at_destination.loc[(recents_at_destination['FL_DATE'] == date)]
            values = filtered_or['DEP_DELAY'].values
            for ft_idx in range(len(dest_features)):
                matrix_dataframe.loc[date, f"{dest_features[ft_idx]}"] = values[ft_idx]


    # Set Departure Delays for cancelled flights to 1440
    matrix_dataframe.loc[(matrix_dataframe['CANCELLED'] != 0), origin_features + carrier_features + carrier_origin_features
                                            + dest_features] = 1440

    # Save the file
    matrix_dataframe.to_csv(f"{out_dir}/D.csv", index=False)
    print(f"File saved: {out_dir}/D.csv")

if __name__ == '__main__':
    if len(sys.argv[1:]) < 7:
        print("There are some parameters of the function are missing.")
        print((sys.argv[1:]))
        exit(1)
    main(*sys.argv[1:])
