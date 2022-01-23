import csv
import functools
import os
import sys
import re


import numpy as np
import pandas as pd
import scipy.stats as stats

from tqdm import tqdm


def write_csv(contents, f_name):
    csv_f = open(f_name, 'w')
    writer = csv.writer(csv_f)
    writer.writerows(contents)
    csv_f.close()


def get_entitlement_per_entity(ents_dir:str, domains:list):

    entitlements_dict = dict()
    
    for domain in domains:
        # Read entailment
        print(f"=========== Reading entailments for domain: {domain} =========== \n")
        ents_df = pd.read_csv(f"{ents_dir}/{domain}_entailments.csv")


        # Join entialments in one string
        
        entitlement_list = ents_df['entailment'].values
        entailments = ''
        for entailment in entitlement_list:
            if entailment != ' ':
                try:
                    entailments += entailment
                except:
                    pass
        # Create dictionary to store all the entailment per entity

        dom_entitlements_dict = dict()

        # Personal Information
        age = re.findall(r'age_\d+', entailments)
        dom_entitlements_dict['Age'] = age

        chest_pain_type = ['TypicalAngina', 'AtypicalAngina', 'NonAnginalPain', 'Asymptomatic']
        dom_entitlements_dict['ChestPainType'] = chest_pain_type
        
        cholesterol = re.findall('chol_\d+', entailments)
        dom_entitlements_dict['Cholesterol'] = cholesterol

        fasting_blood_sugar = ['Higher120mg/dl', 'Lower120mg/dl']
        dom_entitlements_dict['FastingBloodSugar'] = fasting_blood_sugar

        hypertension = ['Hypertensive', 'NonHypertensive']
        dom_entitlements_dict['Hypertension'] = hypertension
        
        rest_blood_pressure = re.findall('rbp_\d+', entailments)
        dom_entitlements_dict['RestBloodPressure'] = rest_blood_pressure

        sex =['Male', 'Female']
        dom_entitlements_dict['Sex'] = sex

        # Exercise ECG Reading

        calblocker =  ['NotUsedClaciumChannelBlocker', 'UsedClaciumChannelBlocker']
        dom_entitlements_dict['CalciumChabbelBlocker'] = calblocker

        betablocker = ['NotUsedBetablocker', 'UsedBetablocker']
        dom_entitlements_dict['Betablocker'] = betablocker
        
        ex_day = re.findall('exday_\d+', entailments)
        dom_entitlements_dict['ExerciseDailyReading'] = ex_day

        digitalis = ['NotUsedDigitalis', 'UsedDigitalis']
        dom_entitlements_dict['Digitalis'] = digitalis

        diuretics = ['NotUsedDiuretics', 'UsedDiuretics']
        dom_entitlements_dict['Diuretics'] = diuretics
        
        ex_dur = re.findall('exdur_\d+', entailments)
        dom_entitlements_dict['ExerciseDuration'] = ex_dur

        ex_peak_height = re.findall('expeakheight_\d+', entailments)
        dom_entitlements_dict['ExerciseHeightAtPeak'] = ex_peak_height
        
        ex_ind_angina = ['InducedAngina', 'NotInduceAngina']
        dom_entitlements_dict['ExerciseInducedAngina'] = ex_ind_angina
        
        ex_ind_hypotension = ['InducedHypotension', 'NonInducedHypotension']
        dom_entitlements_dict['ExerciseInducedHypotension'] = ex_ind_hypotension

        ex_induced_st = re.findall('stdep_\d+', entailments)
        dom_entitlements_dict['ExerciseInducedSTDepression'] = ex_induced_st

        ex_max_heart_rate = re.findall('exmaxhr_\d+', entailments)
        dom_entitlements_dict['ExerciseMaximumHeartRate'] = ex_max_heart_rate

        ex_peak_bp1 = re.findall('expeakbp1_\d+', entailments)
        dom_entitlements_dict['ExercisePeakBloodPressure1'] = ex_peak_bp1

        ex_peak_bp2 = re.findall('expeakbp2_\d+', entailments)
        dom_entitlements_dict['ExercisePeakBloodPressure2'] = ex_peak_bp2

        ex_protocol = ['Bruce','Kottus','McHenry','FastBalke','Balke','Noughton''Bike150kpa/min','Bike125kpa/min','Bike100kpa/min','Bike75kpa/min','Bike50kpa/min']
        dom_entitlements_dict['ExerciseProtocol'] = ex_protocol

        ex_rest_bp = re.findall('exrestbp_\d+', entailments)
        dom_entitlements_dict['ExerciseRestingBloodPressure'] = ex_rest_bp

        ex_rest_heart_rate = re.findall('exminhr_\d+', entailments) 
        dom_entitlements_dict['ExerciseRestingHeartRate'] = ex_rest_heart_rate

        ex_mets = re.findall('met_\d+', entailments)
        dom_entitlements_dict['METSTestScore'] = ex_mets
        
        ex_month = re.findall('exmo_\d+', entailments)
        dom_entitlements_dict['ExerciseMonthlyReading'] = ex_month

        nitrates = ['NotUsedNitrates', 'UsedNitrates']
        dom_entitlements_dict['Nitrates'] = nitrates

        ex_st_dep = ['STWaveAbnormality', 'STWaveNormality', 'VentricularHypertrophy']
        dom_entitlements_dict['STDepression'] = ex_st_dep

        ex_year = re.findall('exyr_\d+', entailments)
        dom_entitlements_dict['ExerciseYearlyReadin'] = ex_year

        # Coronary Angiogram Diagnosis
        ca_day = re.findall('cday_\d+', entailments)
        dom_entitlements_dict['DailyCardiacCath'] = ca_day

        heart_diagnosis = ['PossiblyHealthy''LessThan50DiameterNarrowing','MoreThan50DiameterNarrowing']
        dom_entitlements_dict['HeartDiagnosis'] = heart_diagnosis 

        ca_month = re.findall('camo_\d+', entailments)
        dom_entitlements_dict['MonthlyCardiacCath'] = ca_month

        vessels_dmg = ['0VesselDamaged','1VesselDamaged','2VesselDamaged','3VesselDamaged','1VesselDamaged']
        dom_entitlements_dict['VesselsDamaged'] = vessels_dmg

        ca_year = re.findall('cayr_\d+', entailments)
        dom_entitlements_dict['YearlyyCardiacCath'] = ca_year

        # BloodVesselsDiagnosis

        circumflex = re.findall('cxmain_\d+', entailments)
        dom_entitlements_dict['Circumflex'] = circumflex

        dist_left_anterior = re.findall('laddist_\d+', entailments)
        dom_entitlements_dict['DistalLeftAnteriorDescendingArtery'] = dist_left_anterior

        dist_right_anterior = re.findall('rcadist_\d+', entailments)
        dom_entitlements_dict['DistalRightAnteriorDescendingArtery'] = dist_right_anterior

        left_main_truck = re.findall('lmt_\d+', entailments)
        dom_entitlements_dict['LeftMainTruck'] = left_main_truck
        
        prox_left_anterior = re.findall('ladprox_\d+', entailments)
        dom_entitlements_dict['ProximaLeftAnteriorDescendingArtery'] = prox_left_anterior

        prox_right_anterior = re.findall('rcaprox_\d+', entailments)
        dom_entitlements_dict['ProximaRightAnteriorDescendingArtery'] = prox_right_anterior

        entitlements_dict[domain] = dom_entitlements_dict
        print(f"=========== Finish storing entailments for domain: {domain} =========== \n")

    return entitlements_dict

def existence(value, list2):
    return True if value in list2 else False


        

def main():

    transfer_dir = '/home/juandiri/TFM/Project/Sample/Results/'
    ents_dir = '/home/juandiri/TFM/Project/Sample/Results/Entailments/'
    #domains = ["Cleveland", "Hungary"]
    domains = ["Cleveland", "Hungary", "LongBeach", "Switzerland"]
    correlation_dir = os.path.join(transfer_dir, 'Corr')
    if not os.path.exists(correlation_dir):
        os.mkdir(correlation_dir)
   
    entailment_dictionary = get_entitlement_per_entity(ents_dir, domains)
    #entailment_dictionary = dict()

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

    # Enquiry over entailment closure and explanatory knowledge
    # entailment mapping: 

    
    def ent_existence(source_domain:str, target_domain:str):
        entailment_source = entailment_dictionary[source_domain]
        entailment_target = entailment_dictionary[target_domain]

        entailment_existence = dict()
        for key in entailment_source.keys():
            for value in entailment_target[key]:
                entailment_existence[f"{value}"] = existence(value, entailment_source[key])
        return entailment_existence


    def co_existence_binary(entailment:str, source_domain:str, target_domain:str):
        entailment_existence_target = ent_existence(source_domain, target_domain)
        entailment_existence_source = ent_existence(target_domain, source_domain)
        if entailment in entailment_existence_target.keys() and entailment in entailment_existence_source.keys():
            return 1 if entailment_existence_target[entailment] and entailment_existence_source[entailment] else 0
        else:
            return 0

    def co_existence_quaternary(entailment:str, source_domain:str, target_domain:str):
        entailment_existence_target = ent_existence(source_domain, target_domain)
        entailment_existence_source = ent_existence(target_domain, source_domain)
        if entailment in entailment_existence_target.keys() and entailment in entailment_existence_source.keys():
            if not entailment_existence_target[entailment] and entailment_existence_source[entailment]:
                return 1
            elif entailment_existence_target[entailment] and not entailment_existence_source[entailment]:
                return 2
            elif entailment_existence_target[entailment] and entailment_existence_source[entailment]:
                return 3
            else:
                return 0
        else:
            return 0

    def get_rate(entailment:str, source_domain:str, target_domain):
        eff_df_source = pd.read_csv(f'{ents_dir}/{source_domain}_effective.csv')
        eff_rate_source = eff_df_source.loc[eff_df_source['2'] == entailment, 'rate'].mean()
        imp_df_source = pd.read_csv(f'{ents_dir}/{source_domain}_effective.csv')
        imp_rate_source = imp_df_source.loc[imp_df_source['2'] == entailment, 'rate'].mean()

        eff_df_target = pd.read_csv(f'{ents_dir}/{target_domain}_effective.csv')
        eff_rate_target = eff_df_target.loc[eff_df_target['2'] == entailment, 'rate'].mean()
        imp_df_target = pd.read_csv(f'{ents_dir}/{target_domain}_effective.csv')
        imp_rate_target = imp_df_target.loc[imp_df_target['2'] == entailment, 'rate'].mean()

        eff_rate = (eff_rate_source + eff_rate_target) / 2
        imp_rate = (imp_rate_source + imp_rate_target) / 2
        rate = eff_rate * imp_rate
        return 0 if pd.isna(rate) else rate
    
    entailments_clev = entailment_dictionary['Cleveland']
    entailments_swit = entailment_dictionary['Switzerland']
    entailments_hun = entailment_dictionary['Hungary']
    entailment_lb = entailment_dictionary['LongBeach']

    entailments = [entailments_clev]
    
    out_df = []

    for ents_dict in entailments:
        for key in tqdm(ents_dict.keys()):
            for entailment in ents_dict[key]:
                auc_v = []
                co_ex_v = []
                f = open(os.path.join(correlation_dir, 'tra.csv'), 'r')
                reader = csv.DictReader(f)
                for row in reader:
                    auc = float(row['AUC-FI'])
                    # auc = float(row['ST-AUC-SI'])
                    F_id = row['S-T']
                    [source_domain, target_domain] = F_id.split('-')
                    co_ex = co_existence_quaternary(entailment, source_domain, target_domain)
                    
                    if co_ex == 0:
                        encoding = 0 + get_rate(entailment, source_domain, target_domain)
                        co_ex_v.append(encoding)
                        auc_v.append(auc)
                    if co_ex == 3:
                        encoding = 1 - get_rate(entailment, source_domain, target_domain)
                        co_ex_v.append(encoding)
                        auc_v.append(auc)

                f.close()
                
                try:
                    corr, p_val = stats.pearsonr(co_ex_v, auc_v)
                    if p_val <= 0.05:
                        ## TO FIX
                        plausible = pd.DataFrame([entailment, corr, p_val], columns=['entailment', 'correlation', 'p-value'])
                        print(plausible)
                        out_df = out_df.append(plausible, ignore_index=True)
                        
                    else:
                        
                        pass
                except:
                    pass
            
    
    out_df.to_csv(f"{correlation_dir}/OneEntailment.csv", index=False)

    """    
    def one_entailment(e_mapping:dict):
        ents = e_mapping.keys()
    """


    ### TO DO:
    #
    #  1. Fix and adapt ent_existence, co_existence

        




    

    

if __name__ == '__main__':
    if len(sys.argv[1:]) != 0:
        print("There are some extra parameters.")
        print((sys.argv[1:]))
        exit(1)
    main(*sys.argv[1:])
