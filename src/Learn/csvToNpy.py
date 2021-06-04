import pandas as pd
import numpy as np

d_df = pd.read_csv("/home/juandiri/Desktop/ExplicabilityOntologyBasedML/SampleData/dataXY/AA_ATL_DFW_1500_1759/D.csv")

d_values = d_df.values
np.save("/home/juandiri/Desktop/ExplicabilityOntologyBasedML/SampleData/dataXY/AA_ATL_DFW_1500_1759/D.npy", d_values)