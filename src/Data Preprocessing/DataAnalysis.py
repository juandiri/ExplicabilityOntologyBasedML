import os

import pandas as pd
import numpy as np

from tqdm import tqdm

directory = "/home/juandiri/TFM/TFM/ProcessedData/V1/"

features = ["id", "ccf", "age", "sex", "pain_loc", "pain_exer", "rel_rest", "pain_caden", "cp", "trestbps", "htn", "chol", "smoke", "cigs", "years", "fbs", "dm", "famhist", "restecg", "ekgmo", "ekgday", "ekgyr",
            "dig", "prop", "nitr", "pro", "diuretic", "proto", "thaldur", "thaltime", "met", "thalach", "thalrest", "tpeakbps", "tpeakbpd", "dummy", "trestbpd", "exang", "xhypo", "oldpeak", "slope", "rldv5", "rldv5e",
            "ca", "restckm", "exerckm", "restef", "restwm", "exeref", "exerwm", "thal", "thalsev", "thalpul", "earlobe", "cmo", "cday", "cyr", "num", "lmt", "ladprox", "laddist", "diag", "cxmain",
            "ramus", "om1", "om2", "rcaprox", "rcadist", "lvx1", "lvx2", "lvx3", "lvx4", "lvf", "cathef", "junk", "name"]

out = pd.DataFrame(index=features)

for root, dirs, files in os.walk(directory):
    for file in files:
        with open(f"{directory}/{file}", "r") as f:
            df = pd.read_csv(f)

        non_empty = []
        name = file.split('.')[0]
        for column in df.columns:
            df[column] = df[column].replace(-9, np.NaN)
            if df[column].isna().sum() == 0:
                non_empty.append(column)
            out.loc[column, name] = df[column].isna().sum()

            #print(f"In the column {column}, there are {df[column].isna().sum()} empty values")
        # print(non_empty)
        out_df = df.replace(-9, np.NaN)
        out_df = out_df[["id", "age", "sex", "cp", "trestbps", "htn", "chol", "fbs", "restecg", "ekgmo", "ekgday", "ekgyr",
            "dig", "prop", "nitr", "pro", "diuretic", "proto", "thaldur", "met", "thalach", "thalrest", "tpeakbps", "tpeakbpd", "trestbpd", "exang", "xhypo", "oldpeak", "rldv5e",
            "cmo", "cday", "cyr", "num", "lmt", "ladprox", "laddist", "diag", "cxmain", "rcaprox", "rcadist"]]
        out_df.to_csv(f"/home/juandiri/TFM/TFM/ProcessedData/V2/{file}", index=False)

out.to_csv("MissingValues.csv")
