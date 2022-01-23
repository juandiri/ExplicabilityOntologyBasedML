import os.path
import sys

import pandas as pd

from rdflib import Graph, Literal, BNode, Namespace, URIRef
from rdflib.namespace import RDF, XSD
from tqdm import tqdm


def main(ontology_file, data_dir, out_folder):
    """
    Function that add nodes to the Flight Ontology from csv files

    :param ontology_file: File of the ontology used.
    :param data_dir: Directory containing the data files
    :param out_folder: Output directory
    """

    def add_patient(data_csv_file):

        # Create dataframe
        dataframe = pd.read_csv(data_csv_file)

        # For each line of data, we add the patient instances according to the ontology
        for index, row in tqdm(dataframe.iterrows()):

            # Generate graph
            rdf = Graph()
            # Add ontology to file
            rdf.parse(ontology_file, format="xml")
            # Bind namespace to prefix
            rdf.bind("hrt", hrt)

            ## ADDING EACH ENTITY INSTANCE TO THE ONTOLOGY AND RELATE EACH OTHER ACCORDINGLY
            # REMARK!!: The check for 'value == value' is made to remove nan values

            # Create instance for patient
            uri_patient = URIRef(f"{hrt}patient_{int(row['id'])}")
            rdf.add((uri_patient, RDF["type"], hrt["Patient"]))

            # Add Personal Information and related entities
            uri_perinfo = URIRef(hrt + "perinfo_patient_" + str(int(row['id'])))
            rdf.add((uri_perinfo, RDF['type'], hrt['PersonalInformation']))

            ## Add the age
            if row["age"] is not None and row["age"] == row["age"]:
                try:
                    uri_age = hrt[f"age_{int(row['age'])}"]
                except:
                    uri_age = URIRef(f"{hrt}age_{int(row['age'])}")
                rdf.add((uri_age, RDF['type'], hrt['Age']))
                # Link with patient
                rdf.add((uri_perinfo, hrt['PersonalInformationContains'], uri_age))

            ## Add sex
            if row["sex"] is not None and row["sex"] == row["sex"]:
                if row["sex"] == 0:
                    uri_sex = hrt['Female']
                else: 
                    uri_sex = hrt['Male']
                rdf.add((uri_sex, RDF['type'], hrt['Sex']))
                # Link with patient
                rdf.add((uri_perinfo, hrt['PersonalInformationContains'], uri_sex))

            # Add Chest Pain Type
            if row["cp"] is not None and row["cp"] == row["cp"]:
                if int(row["cp"]) == 1:
                    uri_cp = hrt['TypicalAngina']
                elif int(row["cp"]) == 2:
                    uri_cp = hrt['AtypicalAngina']
                elif int(row["cp"]) == 3:
                    uri_cp = hrt['NonAnginaPain']
                else:
                    uri_cp = hrt['Asymptomatic']
                rdf.add((uri_cp, RDF['type'], hrt['ChestPainType']))
                # Link with patient
                rdf.add((uri_perinfo, hrt['PersonalInformationContains'], uri_cp))

            ## Add Resting Blood Pressure
            if row["trestbps"] is not None and row["trestbps"] == row["trestbps"]:
                try:
                    uri_restbp = hrt[f"rbp_{int(row['trestbps'])}"]
                except:
                    uri_restbp = URIRef(f"{hrt}rbp_{int(row['trestbps'])}")
                rdf.add((uri_restbp, RDF['type'], hrt['RestingSystolicBloodPressure']))
                # Link with patient
                rdf.add((uri_perinfo, hrt['PersonalInformationContains'], uri_restbp))
            
            ## Add Hypertension              
            if row["htn"] is not None and row["htn"] == row["htn"]:
                if int(row['htn']) == 1:
                    uri_hypertension = hrt['Hypertensive']
                else:
                    uri_hypertension = hrt['NonHypertensive']
                rdf.add((uri_hypertension, RDF["type"], hrt['Hypertension']))
                # Link with patient
                rdf.add((uri_perinfo, hrt['PersonalInformationContains'], uri_hypertension))
                
            ## Add Cholesterol
            if row["chol"] is not None and row["chol"] == row["chol"]:
                try:
                    uri_chol = hrt[f"chol_{int(row['chol'])}"]
                except:
                    uri_chol = URIRef(f"{hrt}chol_{int(row['chol'])}")
                rdf.add((uri_chol, RDF["type"], hrt['Cholesterol']))
                # Link with patient
                rdf.add((uri_perinfo, hrt['PersonalInformationContains'], uri_chol))

            ## Add Fasting Blood Sugar    
            if row["fbs"] is not None and row["fbs"] == row["fbs"]:
                if int(row["fbs"]) == 1:
                    uri_fbs = hrt['Higher120mg/dl']
                else:
                    uri_fbs = hrt['Lower120mg/dl']
                rdf.add((uri_fbs, RDF['type'], hrt['FastingBloodSugar']))
                # Link with patient
                rdf.add((uri_perinfo, hrt['PersonalInformationContains'], uri_fbs))

            # Link Personal Information with patient
            rdf.add((uri_patient, hrt['hasPersonalInformation'], uri_perinfo))

            # Add ECG reading and related entities
            uri_ecg = URIRef(hrt + "ecg_patient_" + str(int(row['id'])))
            rdf.add((uri_ecg, RDF['type'], hrt['ExerciseECGReading']))

            ## Add ST Depression
            if row['restecg'] is not None and row['restecg'] == row['restecg']:
                if int(row['restecg']) == 0:
                    uri_st = hrt['STWaveNormality']
                elif int(row['restecg']) == 1:
                    uri_st = hrt['STWaveAbnormality']
                else:
                    uri_st = hrt['VentricularHypertrophy']
                rdf.add((uri_st, RDF['type'], hrt['STDepression']))
                # Link with ECG reading
                rdf.add((uri_ecg, hrt['ECGcontains'], uri_protocol))
                

            ## Add Exercise Protocol
            if row["proto"] is not None and row["proto"] == row["proto"]:
                if int(row["proto"]) == 1:
                    uri_protocol = hrt['Bruce']
                elif int(row["proto"] == 2):
                    uri_protocol = hrt['Kottus']
                elif int(row["proto"]) == 3:
                    uri_protocol = hrt['McHenry']
                elif int(row["proto"]) == 4:
                    uri_protocol = hrt['FastBalke']
                elif int(row["proto"]) == 5:
                    uri_protocol = hrt['Balke']
                elif int(row["proto"]) == 6:
                    uri_protocol = hrt['Noughton']
                elif int(row["proto"]) == 7:
                    uri_protocol = hrt['Bike150kpa/min']
                elif int(row["proto"]) == 8:
                    uri_protocol = hrt['Bike125kpa/min']
                elif int(row["proto"]) == 9:
                    uri_protocol = hrt['Bike100kpa/min']
                elif int(row["proto"]) == 10:
                    uri_protocol = hrt['Bike75kpa/min']
                elif int(row["proto"]) == 11:
                    uri_protocol = hrt['Bike50kpa/min']
                else:
                    uri_protocol = hrt['ArmErgometer']
                rdf.add((uri_protocol, RDF['type'], hrt['ExerciseProtocol']))
                # Link with ECG reading
                rdf.add((uri_ecg, hrt['ECGcontains'], uri_protocol))
            
            ## Add Exercise Duration
            if row["thaldur"] is not None and row["thaldur"] == row["thaldur"]:
                try:
                    uri_exdur = hrt[f"exdur_{row['thaldur']}"]
                except:
                    uri_exdur = URIRef(f"{hrt}exdur_row['thaldur']")
                rdf.add((uri_exdur, RDF['type'], hrt['ExerciseDuration']))
                ## Link with ECG reading
                rdf.add((uri_ecg, hrt['ECGcontains'],uri_exdur))
            
            ## Add Exercise Induced Angina
            if row["exang"] is not None and row["exang"] == row["exang"]:
                if int(row["exang"]) == 1:
                    uri_exang = hrt['InducedAngina']
                else:
                     uri_exang = hrt['NotInducedAngina']
                rdf.add((uri_exdur, RDF['type'], hrt['ExerciseInducedAngina']))
                ## Link with ECG reading
                rdf.add((uri_ecg, hrt['ECGcontains'],uri_exang))

            ## Add Exercise Induced Hypotension    
            if row["xhypo"] is not None and row["xhypo"] == row["xhypo"]:
                if int(row["xhypo"]) == 1:
                    uri_exhypo = hrt['InducedHypotension']
                else:
                    uri_exhypo = hrt['NonInducedHypotension']
                rdf.add((uri_exhypo, RDF['type'], hrt['ExerciseInducedHypoyension']))
                ## Link with ECG reading
                rdf.add((uri_ecg, hrt['ECGcontains'],uri_exhypo))

            ## Add Exercise Induced ST Depression
            if row["oldpeak"] is not None and row["oldpeak"] == row["oldpeak"]:
                try:
                    uri_stdep = hrt[f"stdep_{row['oldpeak']}"]
                except:
                    uri_stdep = URIRef(f"{hrt}stdep_{row['oldpeak']}")
                rdf.add((uri_stdep, RDF['type'], hrt['ExerciseInducedSTDepression']))
                ## Link with ECG reading
                rdf.add((uri_ecg, hrt['ECGcontains'],uri_stdep))

            ## Add Exercise Monthly Reading    
            if row["ekgmo"] is not None and row["ekgmo"] == row["ekgmo"]:
                try:
                    uri_exmo = hrt[f"exmo_{int(row['ekgmo'])}"]
                except:
                    uri_exmo = URIRef(f"{hrt}exmo_{int(row['ekgmo'])}")
                rdf.add((uri_exmo, RDF['type'], hrt['MonthlyReading']))
                ## Link with ECG reading
                rdf.add((uri_ecg, hrt['ECGcontains'],uri_exmo))

            ## Add Exercise Daily Reading    
            if row["ekgday"] is not None and row["ekgday"] == row["ekgday"]:
                try:
                    uri_exday = hrt[f"exday_{int(row['ekgday'])}"]
                except:
                    uri_exday = URIRef(f"{hrt}exday_{int(row['ekgday'])}")
                rdf.add((uri_exday, RDF['type'], hrt['DailyReading']))
                ## Link with ECG reading
                rdf.add((uri_ecg, hrt['ECGcontains'],uri_exday))

            ## Add Exercise Yearly Reading    
            if row["ekgyr"] is not None and row["ekgyr"] == row["ekgyr"]:
                try:
                    uri_exyr = hrt[f"exyr_{int(row['ekgyr'])}"]
                except:
                    uri_exyr = URIRef(f"{hrt}exyr_{int(row['ekgyr'])}")
                rdf.add((uri_exyr, RDF['type'], hrt['YearlyReading']))
                ## Link with ECG reading
                rdf.add((uri_ecg, hrt['ECGcontains'],uri_exyr))

            ## Add Exercise METS Test Score   
            if row["met"] is not None and row["met"] == row["met"]:
                try:
                    uri_mets = hrt[f"mets_{int(row['met'])}"]
                except:
                    uri_mets = URIRef(f"{hrt}mets_{int(row['met'])}")
                rdf.add((uri_mets, RDF['type'], hrt['METSTestScore']))
                ## Link with ECG reading
                rdf.add((uri_ecg, hrt['ECGcontains'],uri_mets))

            ## Add Exercise Maximum Heart Rate  
            if row["thalach"] is not None and row["thalach"] == row["thalach"]:
                try:
                    uri_exmaxhrt = hrt[f"exmaxhr_{int(row['thalach'])}"]
                except:
                    uri_exmaxhrt = URIRef(f"{hrt}exmaxhr_{int(row['thalach'])}")
                rdf.add((uri_exmaxhrt, RDF['type'], hrt['ExerciseMaximumHeartRate']))
                ## Link with ECG reading
                rdf.add((uri_ecg, hrt['ECGcontains'],uri_exmaxhrt))

            ## Add Exercise Resting Heart Rate  
            if row["thalrest"] is not None and row["thalrest"] == row["thalrest"]:
                try:
                    uri_exresthrt = hrt[f"exminhr_{int(row['thalrest'])}"]
                except:
                    uri_exresthrt = URIRef(f"{hrt}exminhr_{int(row['thalrest'])}")
                rdf.add((uri_exresthrt, RDF['type'], hrt['ExerciseRestingHeartRate']))
                ## Link with ECG reading
                rdf.add((uri_ecg, hrt['ECGcontains'],uri_exresthrt))

            ## Add Exercise Peak Blood Pressure 1  
            if row["tpeakbps"] is not None and row["tpeakbps"] == row["tpeakbps"]:
                try:
                    uri_expeakbp1 = hrt[f"expeakbp1_{int(row['tpeakbps'])}"]
                except:
                    uri_expeakbp1 = URIRef(f"{hrt}expeakbp1_{int(row['tpeakbps'])}")
                rdf.add((uri_expeakbp1, RDF['type'], hrt['ExercisePeakBloodPressure1']))
                ## Link with ECG reading
                rdf.add((uri_ecg, hrt['ECGcontains'],uri_expeakbp1))
            
            ## Add Exercise Peak Blood Pressure 2
            if row["tpeakbpd"] is not None and row["tpeakbpd"] == row["tpeakbpd"]:
                try:
                    uri_expeakbp2 = hrt[f"expeakbp2_{int(row['tpeakbpd'])}"]
                except:
                    uri_expeakbp2 = URIRef(f"{hrt}expeakbp2_{int(row['tpeakbpd'])}")
                rdf.add((uri_expeakbp2, RDF['type'], hrt['ExercisePeakBloodPressure2']))
                ## Link with ECG reading
                rdf.add((uri_ecg, hrt['ECGcontains'],uri_expeakbp2))

            ## Add Exercise Resting Blood Pressure
            if row["trestbpd"] is not None and row["trestbpd"] == row["trestbpd"]:
                try:
                    uri_exrestbp = hrt[f"exrestbp_{int(row['trestbpd'])}"]
                except:
                    uri_exrestbp = URIRef(f"{hrt}exrestbp_{int(row['trestbpd'])}")
                rdf.add((uri_exrestbp, RDF['type'], hrt['ExerciseRestingBloodPressure']))
                ## Link with ECG reading
                rdf.add((uri_ecg, hrt['ECGcontains'],uri_exrestbp))

            ## Add Exercise Peak Height
            if row["rldv5e"] is not None and row["rldv5e"] == row["rldv5e"]:
                try:
                    uri_expeakheight = hrt[f"expeakheight_{int(row['rldv5e'])}"]
                except:
                    uri_expeakheight = URIRef(f"{hrt}expeakheight_{int(row['rldv5e'])}")
                rdf.add((uri_expeakheight, RDF['type'], hrt['ExerciseHeightAtPeak']))
                ## Link with ECG reading
                rdf.add((uri_ecg, hrt['ECGcontains'],uri_expeakheight))

            ## Add Use of Digitalis
            if row["dig"] is not None and row["dig"] == row["dig"]:
                if row["dig"] == 1:
                    uri_dig = hrt['UsedDigitalis']
                else: 
                    uri_dig = hrt['NotUsedDigitalis']
                rdf.add((uri_dig, RDF['type'], hrt['Digitalis']))
                ## Link with ECG reading
                rdf.add((uri_dig, hrt['ECGcontains'], uri_dig))
            
            ## Add Use of Betablocker
            if row["prop"] is not None and row["prop"] == row["prop"]:
                if row["prop"] == 1:
                    uri_bb = hrt['UsedBetablocker']
                else: 
                    uri_bb = hrt['NotUsedBetablocker']
                rdf.add((uri_bb, RDF['type'], hrt['Betablocker']))
                ## Link with ECG reading
                rdf.add((uri_ecg, hrt['ECGcontains'], uri_bb))

            ## Add Use of Nitrates
            if row["nitr"] is not None and row["nitr"] == row["nitr"]:
                if row["nitr"] == 1:
                    uri_nit = hrt['UsedNitrates']
                else: 
                    uri_nit = hrt['NotUsedNitrates']
                rdf.add((uri_nit, RDF['type'], hrt['Nitrates']))
                ## Link with ECG reading
                rdf.add((uri_ecg, hrt['ECGcontains'], uri_nit))

            ## Add Use of Calcium Channel Blocker
            if row["pro"] is not None and row["pro"] == row["pro"]:
                if row["pro"] == 1:
                    uri_ccb = hrt['UsedCalciumChannelBlocker']
                else: 
                    uri_ccb = hrt['NotUsedCalciumChannelBlocker']
                rdf.add((uri_ccb, RDF['type'], hrt['CalciumChannelBlocker']))
                ## Link with ECG reading
                rdf.add((uri_ecg, hrt['ECGcontains'], uri_ccb))
            
            ## Add Use of Diuretics
            if row["diuretic"] is not None and row["diuretic"] == row["diuretic"]:
                if row["diuretic"] == 1:
                    uri_diur = hrt['UsedDiuretics']
                else: 
                    uri_diur = hrt['NotUsedDiuretics']
                rdf.add((uri_diur, RDF['type'], hrt['Diuretics']))
                ## Link with ECG reading
                rdf.add((uri_ecg, hrt['ECGcontains'], uri_diur))
          
            # Link ECG Reading with patient
            rdf.add((uri_patient, hrt['hasExerciseECGReading'], uri_ecg))

            ### Add Coronoary Angiograms and related entities
            uri_ca = URIRef(hrt + "ca_patient_" + str(int(row['id'])))
            rdf.add((uri_ca, RDF['type'], hrt['CoronaryAngiogramsDiagnosis']))

            ## Add Monthly Coronoary Angiograms    
            if row["cmo"] is not None and row["cmo"] == row["cmo"]:
                try:
                    uri_camo = hrt[f"camo_{int(row['cmo'])}"]
                except:
                    uri_camo = URIRef(f"{hrt}camo_{int(row['cmo'])}")
                rdf.add((uri_camo, RDF['type'], hrt['MonthlyCardiacCath']))
                ## Link with Coronoary Angiograms
                rdf.add((uri_ca, hrt['CoronaryAngiogramsContains'],uri_camo))

            ## Add Daily Coronoary Angiograms
            if row["cday"] is not None and row["cday"] == row["cday"]:
                try:
                    uri_caday = hrt[f"cday_{int(row['cday'])}"]
                except:
                    uri_caday = URIRef(f"{hrt}cday_{int(row['cday'])}")
                rdf.add((uri_caday, RDF['type'], hrt['DailyCardiacCath']))
                ### Link with Coronoary Angiograms
                rdf.add((uri_ca, hrt['CoronaryAngiogramsContains'],uri_caday))

            ### Add Yearly Coronoary Angiograms 
            if row["cyr"] is not None and row["cyr"] == row["cyr"]:
                try:
                    uri_cayr = hrt[f"cayr_{int(row['cyr'])}"]
                except:
                    uri_cayr = URIRef(f"{hrt}cayr_{int(row['cyr'])}")
                rdf.add((uri_cayr, RDF['type'], hrt['YearlyCardiacCath']))
                ### Link with Coronoary Angiograms
                rdf.add((uri_ca, hrt['CoronaryAngiogramsContains'],uri_cayr))

            ### Add Nummber of Vessels Damaged

            if row["num"] is not None and row['num'] == row['num']:
                if row["num"] == 0:
                    uri_vessdmg = hrt['0VesselDamaged']
                elif row["num"] == 1:
                    uri_vessdmg = hrt['1VesselDamaged']
                elif row["num"] == 2:
                    uri_vessdmg = hrt['2VesselDamaged']
                elif row["num"] == 3:
                    uri_vessdmg = hrt['3VesselDamaged']
                else:
                    uri_vessdmg = hrt['1VesselDamaged']
                
                rdf.add((uri_ca, hrt['CoronaryAngiogramsContains'], uri_vessdmg))
            
            ### Add Heart Diagnosis (target)
            if row["target"] is not None and row["target"] == row["target"]:
                if row["target"] == 0:
                    uri_diagnosis = hrt['PossiblyHealthy']
                elif row["target"] == 1:
                    uri_diagnosis = hrt['LessThan50DiameterNarrowing']
                else: 
                    uri_diagnosis = hrt['MoreThan50DiameterNarrowing']

                rdf.add((uri_diagnosis, RDF['type'], hrt['HeartDiseaseDiagnosis']))
                ### Link with Coronoary Angiograms
                rdf.add((uri_ca, hrt['CoronaryAngiogramsContains'], uri_diagnosis))
                rdf.add((uri_patient, hrt['hasHeartDiseaseDiagnosis'], uri_diagnosis))

            # Link Coronoary Angiograms with patient
            rdf.add((uri_patient, hrt['hasCoronaryAngiogramsDiagnosis'], uri_ca))


            #### Add Blood Vessels Diagnosis data properties
            uri_bv = URIRef(hrt + "bv_patient_" + str(int(row['id'])))
            rdf.add((uri_bv, RDF['type'], hrt['BloodVesselsDiagnosis']))

            #### Add Left Main Truck
            if row["lmt"] is not None and row["lmt"] == row["lmt"]:
                try:
                    uri_lmt = hrt[f"lmt_{int(row['lmt'])}"]
                except:
                    uri_lmt = URIRef(f"{hrt}lmt_{int(row['lmt'])}")
                rdf.add((uri_lmt, RDF['type'], hrt['LeftMainTruck']))
                #### Link with Blood Vessels Diagnosis
                rdf.add((uri_bv, hrt['BloodVesselsDiagnosisContains'],uri_lmt))

            #### Add Proximal Left Anterior Descending Artery
            if row["ladprox"] is not None and row["ladprox"] == row["ladprox"]:
                try:
                    uri_ladprox = hrt[f"ladprox_{int(row['ladprox'])}"]
                except:
                    uri_ladprox = URIRef(f"{hrt}ladprox_{int(row['ladprox'])}")
                rdf.add((uri_ladprox, RDF['type'], hrt['ProximalLeftAnteriorDescendingArtery']))
                #### Link with Blood Vessels Diagnosis
                rdf.add((uri_bv, hrt['BloodVesselsDiagnosisContains'],uri_ladprox))
            
            #### Add Distal Left Anterior Descending Artery
            if row["laddist"] is not None and row["laddist"] == row["laddist"]:
                try:
                    uri_laddist = hrt[f"laddist_{int(row['laddist'])}"]
                except:
                    uri_laddist = URIRef(f"{hrt}laddist_{int(row['laddist'])}")
                rdf.add((uri_laddist, RDF['type'], hrt['DistalLeftAnteriorDescendingArtery']))
                #### Link with Blood Vessels Diagnosis
                rdf.add((uri_bv, hrt['BloodVesselsDiagnosisContains'],uri_laddist))

             #### Add Circumflex
            if row["cxmain"] is not None and row["cxmain"] == row["cxmain"]:
                try:
                    uri_cxmain = hrt[f"cxmain_{int(row['cxmain'])}"]
                except:
                    uri_cxmain = URIRef(f"{hrt}cxmain_{int(row['cxmain'])}")
                rdf.add((uri_cxmain, RDF['type'], hrt['Circumflex']))
                #### Link with Blood Vessels Diagnosis
                rdf.add((uri_bv, hrt['BloodVesselsDiagnosisContains'],uri_cxmain))

            #### Add Proximal Right Anterior Descending Artery
            if row["rcaprox"] is not None and row["rcaprox"] == row["rcaprox"]:
                try:
                    uri_rcaprox = hrt[f"rcaprox_{int(row['rcaprox'])}"]
                except:
                    uri_rcaprox = URIRef(f"{hrt}rcaprox_{int(row['rcaprox'])}")
                rdf.add((uri_rcaprox, RDF['type'], hrt['ProximalRightAnteriorDescendingArtery']))
                #### Link with Blood Vessels Diagnosis
                rdf.add((uri_bv, hrt['BloodVesselsDiagnosisContains'],uri_rcaprox))
            
            #### Add Distal Right Anterior Descending Artery
            if row["rcadist"] is not None and row["rcadist"] == row["rcadist"]:
                try:
                    uri_rcadist = hrt[f"rcadist_{int(row['rcadist'])}"]
                except:
                    uri_rcadist = URIRef(f"{hrt}rcadist_{int(row['rcadist'])}")
                rdf.add((uri_rcadist, RDF['type'], hrt['DistalRightAnteriorDescendingArtery']))
                #### Link with Blood Vessels Diagnosis
                rdf.add((uri_bv, hrt['BloodVesselsDiagnosisContains'],uri_rcadist))

            # Link Blood Vessels Diagnosis with patient
            rdf.add((uri_patient, hrt['hasBloodVesselsDiagnosis'], uri_bv))           

            # Save an OWL file for each location
            with open(f"{out_folder}/{file_name}_{int(row['id'])}.owl", "w+") as f:
                f.write(rdf.serialize(format="xml"))
            print(f"Saved file {out_folder}/{file_name}_{int(row['id'])}.owl")
            

    # Set up namespace used
    hrt = Namespace("http://www.semanticweb.org/juandiri/ontologies/2021/9/untitled-ontology-7#")

    # Dictionaty to store file paths corresponding to
    # departures and meteorological data path for each year
    data = dict()

    # Set up the data directory
    data_directory = os.path.join(data_dir)

    # For each data file, insert the instances to the ontology
    for root, dirs, files in tqdm(os.walk(data_directory)):
        for file in tqdm(files):
            # Save file name and format
            [file_name, f_format] = os.path.basename(file).split(".")
            if f_format == "csv":
                # Add instances to the ontology from csv file
                add_patient(f"{data_directory}/{file}")
                


if __name__ == "__main__":
    if len(sys.argv[1:]) != 3:
        print("There are some parameters of the function are missing.")
        print((sys.argv[1:]))
        exit(1)
    main(*sys.argv[1:])
