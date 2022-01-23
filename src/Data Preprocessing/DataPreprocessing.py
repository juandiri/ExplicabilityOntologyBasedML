import pandas as pd

data = []
with open("/home/juandiri/Desktop/TFM/RawData/hungarian.data") as f:

    lines = f.read()
    lines = lines.replace('\n', ' ')

rows = lines.split('name')

for row in rows:
    row = row.split(' ')
    row[-1] = 'name'
    if len(row) == 77:
        row.pop(0)
        data.append(row)

features = ["id", "ccf", "age", "sex", "pain_loc", "pain_exer", "rel_rest", "pain_caden", "cp", "trestbps", "htn", "chol", "smoke", "cigs", "years", "fbs", "dm", "famhist", "restecg", "ekgmo", "ekgday", "ekgyr",
            "dig", "prop", "nitr", "pro", "diuretic", "proto", "thaldur", "thaltime", "met", "thalach", "thalrest", "tpeakbps", "tpeakbpd", "dummy", "trestbpd", "exang", "xhypo", "oldpeak", "slope", "rldv5", "rldv5e",
            "ca", "restckm", "exerckm", "restef", "restwm", "exeref", "exerwm", "thal", "thalsev", "thalpul", "earlobe", "cmo", "cday", "cyr", "num", "lmt", "ladprox", "laddist", "diag", "cxmain",
            "ramus", "om1", "om2", "rcaprox", "rcadist", "lvx1", "lvx2", "lvx3", "lvx4", "lvf", "cathef", "junk", "name"]
df = pd.DataFrame(data, columns=features)
df.to_csv("Hungary.csv", index=False)
