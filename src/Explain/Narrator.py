import csv
import os
import sys

import numpy as np

def main():

    transfer_dir = '/home/juandiri/TFM/TFM/Sample/Results'
    correlation_dir = os.path.join(transfer_dir, 'Corr')
    if not os.path.exists(correlation_dir):
        os.mkdir(correlation_dir)

    def write_csv(contents, f_name):
        csv_f = open(f_name, 'w')
        writer = csv.writer(csv_f)
        writer.writerows(contents)
        csv_f.close()


    # Auxiliary funtion that extract feature specificity/generality indexes (SI/GI)
    # calculate feature transferability index (TI)
    def get_indices():
        print('--------- Calculate Transferability Indexes -------------')
        HT_Dir = os.path.join(transfer_dir, 'HT_Result')
        ST_Dir = os.path.join(transfer_dir, 'ST_Result')
        S_Dir = os.path.join(transfer_dir, 'Trained')
        domains = os.listdir(S_Dir)
        R_Beta = {}
        for domain in domains:
            r_beta = np.load(os.path.join(S_Dir, domain, 'local_test_res.npy'))
            R_Beta[domain] = np.average(r_beta, axis=0)
        header = ['S-T', 'T-ACC', 'T-AUC', 'HT-ACC', 'HT-AUC', 'HT-ACC-SI', 'HT-AUC-SI', 'ST-ACC', 'ST-AUC', 'ST-ACC-SI',
                'ST-AUC-SI', 'ACC-FI', 'AUC-FI']
        lines = [header]
        for i, d1 in enumerate(domains):
            if i % 10 == 0:
                print('i: %d ' % i)
            for d2 in domains:
                tra = '%s-%s' % (d1, d2)
                tra_f = '%s.npy' % tra
                print(tra_f)
                if os.path.exists(os.path.join(HT_Dir, tra_f)) and os.path.exists(os.path.join(ST_Dir, tra_f)):
                    r_ht = np.average(np.load(os.path.join(HT_Dir, tra_f)), axis=0)
                    r_st = np.average(np.load(os.path.join(ST_Dir, tra_f)), axis=0)
                    line = [tra] + list(R_Beta[d2]) + list(r_ht) + list((R_Beta[d2] - r_ht) / r_ht) + list(r_st) + list(
                        (r_st - R_Beta[d2]) / R_Beta[d2]) + list((r_st - R_Beta[d2]) / R_Beta[d2] - (R_Beta[d2] - r_ht) / r_ht)
                    lines.append(line)
        
        write_csv(lines, os.path.join(correlation_dir, 'tra.csv'))

    #get_indices()

if __name__ == '__main__':
    if len(sys.argv[1:]) != 0:
        print("There are some extra parameters.")
        print((sys.argv[1:]))
        exit(1)
    main(*sys.argv[1:])
