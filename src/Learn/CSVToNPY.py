import pandas as pd
import numpy as np

d_df = pd.read_csv("/home/juandiri/TFM/TFM/Sample/Hungary/D.csv")

d_values = d_df.values
np.save("/home/juandiri/TFM/TFM/Sample/Hungary/D.npy", d_values)
