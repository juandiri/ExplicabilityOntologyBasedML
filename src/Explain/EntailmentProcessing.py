import csv
import os
import sys
import re

import numpy as np
import pandas as pd
import scipy.stats as stats

def squeeze_nan(x):
            original_columns = x.index.tolist()

            squeezed = x.dropna()

            if squeezed.count() != 3:
                #print(squeezed.count())
                squeezed['2'] = np.NaN
                #print(squeezed)
                #input()
                squeezed.index = [1, 2, 0]
                #print(squeezed)
            else:
                pass

            return squeezed.reindex(original_columns, fill_value=' ')

def get_entailments(ents_dir:str, outdir:str, domains:list):
    for domain in domains:
        # Read entailment
        print(f"=========== Reading entailment for domain: {domain} =========== \n")

        eff_ents_df = pd.read_csv(f"{ents_dir}/{domain}_eff.csv", names=['entailment', 'rate'], sep=':')
        eff_ents_df_expanded = eff_ents_df['entailment'].str.split(',', expand=True)
        eff_ents_df_expanded =  eff_ents_df_expanded.apply(squeeze_nan, axis=1)
        eff_ents_df_expanded['rate'] = eff_ents_df['rate'].str.split(',', expand=True)[1]
        eff_ents_df_expanded.to_csv(f'{outdir}/{domain}_effective.csv', index=False)
        print(f"=========== Saving effective entailments =========== \n")

        imp_ents_df = pd.read_csv(f"{ents_dir}/{domain}_imp.csv", names=['entailment', 'rate'], sep =':')
        imp_ents_df_expanded = imp_ents_df['entailment'].str.split(',', expand=True)
        imp_ents_df_expanded =  imp_ents_df_expanded.apply(squeeze_nan, axis=1)
        imp_ents_df_expanded['rate'] = imp_ents_df['rate']
        imp_ents_df_expanded.to_csv(f'{outdir}/{domain}_important.csv', index=False)
        print(f"=========== Saving important entailments =========== \n")

        ents_df = eff_ents_df_expanded.append(imp_ents_df_expanded)
        ents_df = ents_df.drop_duplicates(subset= pd.Index([1, 2]))

        ents_df['entailment'] = ents_df[0] + ents_df[1] + ents_df[2]
        ents_df['entailment'].to_csv(f'{outdir}/{domain}_entailments.csv', index=False)
        print(f"=========== Saving entailments =========== \n")

        print(f"=========== Finish storing entailments for domain: {domain} =========== \n\n")
    

ents_dir = '/home/juandiri/TFM/Project/RDFInsertions/4/Entailments'
out_dir = '/home/juandiri/TFM/Project/Sample/Results/Entailments'
domains = ["Cleveland", "Hungary", "LongBeach", "Switzerland"]

get_entailments(ents_dir, out_dir, domains)

