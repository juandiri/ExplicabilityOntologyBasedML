import csv
import os
import sys

import numpy as np
import pandas as pd

from tqdm import tqdm


def main():

    data_dir = "/home/juandiri/TFM/TFM/ProcessedData/V2/Switzerland.csv"
    out_dir = "/home/juandiri/TFM/TFM/Sample/Switzerland"

    # Dataframe to store the data
    features = ['num','id','age','sex','cp','trestbps','htn','chol','fbs','restecg','ekgmo','ekgday','ekgyr','dig','prop','nitr','pro','diuretic','proto','thaldur','met','thalach','thalrest','tpeakbps','tpeakbpd','trestbpd','exang','xhypo','oldpeak','rldv5e','cmo','cday','cyr', 'lmt','ladprox','laddist','diag','cxmain','rcaprox','rcadist']
    matrix_dataframe = pd.DataFrame(columns=features)

    try:
        dataframe = pd.read_csv(data_dir)
        matrix_dataframe = dataframe
        matrix_dataframe['num'] = matrix_dataframe['num'].replace([2,3,4], 1)
        matrix_dataframe = matrix_dataframe.replace(np.NaN, -9)
        matrix_dataframe.to_csv(f"{out_dir}/D.csv", index=False)

    except Exception as e:
        raise e
                        



                        





if __name__ == '__main__':
    if len(sys.argv[1:]) != 0:
        print("There are some parameters of the function are missing.")
        print((sys.argv[1:]))
        exit(1)
    main(*sys.argv[1:])
