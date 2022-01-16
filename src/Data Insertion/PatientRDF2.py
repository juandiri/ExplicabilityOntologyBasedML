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

            # Create instance for patient
            uri_patient = URIRef(hrt + "patient_" + str(int(row['id'])))
            rdf.add((uri_patient, RDF["type"], hrt["Patient"]))

            
            
            
            # Add patient data properties



            if row["age"] is not None and row["age"] == row["age"]:
                rdf.add((uri_patient, hrt["hasAge"], Literal(int(row["age"]), datatype=XSD["integer"])))
            if row["sex"] is not None and row["sex"] == row["sex"]:
                if row["sex"] == 0:
                    rdf.add((uri_patient, hrt["hasSex"], Literal("Female", datatype=XSD["string"])))
                else:
                    rdf.add((uri_patient, hrt["hasSex"], Literal("Male", datatype=XSD["string"])))
            if row["cp"] is not None and row["cp"] == row["cp"]:
                if row["cp"] == 1:
                    rdf.add((uri_patient, hrt["hasChestPainType"], Literal("TypicalAngina", datatype=XSD["string"])))
                elif row["cp"] == 2:
                    rdf.add((uri_patient, hrt["hasChestPainType"], Literal("AtypicalAngina", datatype=XSD["string"])))
                elif row["cp"] == 3:
                    rdf.add((uri_patient, hrt["hasChestPainType"], Literal("NonAnginaPain", datatype=XSD["string"])))
                else:
                    rdf.add((uri_patient, hrt["hasChestPainType"], Literal("Asymptomatic", datatype=XSD["string"])))

            if row["trestbps"] is not None and row["trestbps"] == row["trestbps"]:
                rdf.add((uri_patient, hrt["hasRestingSystolicBloodPressure"], Literal(int(row["trestbps"]), datatype=XSD["integer"])))
            if row["htn"] is not None and row["htn"] == row["htn"]:
                if int(row['htn']) == 1:
                    rdf.add((uri_patient, hrt["hasHypertension"], Literal("true", datatype=XSD["boolean"])))
                else:
                    rdf.add((uri_patient, hrt["hasHypertension"], Literal("false", datatype=XSD["boolean"])))
            if row["chol"] is not None and row["chol"] == row["chol"]:
                rdf.add((uri_patient, hrt["hasCholesterol"], Literal(int(row["chol"]), datatype=XSD["integer"])))
            if row["fbs"] is not None and row["fbs"] == row["fbs"]:
                if int(row["fbs"]) == 1:
                    rdf.add((uri_patient, hrt["hasHighFastingBloodSugar"], Literal("true", datatype=XSD["boolean"])))
                else:
                    rdf.add((uri_patient, hrt["hasHighFastingBloodSugar"], Literal("false", datatype=XSD["boolean"])))
            if row["proto"] is not None and row["proto"] == row["proto"]:
                if row["proto"] == 1:
                    rdf.add((uri_patient, hrt["hasExerciseProtocol"], Literal("Bruce", datatype=XSD["string"])))
                elif row["proto"] == 2:
                    rdf.add((uri_patient, hrt["hasExerciseProtocol"], Literal("Kottus", datatype=XSD["string"])))
                elif row["proto"] == 3:
                    rdf.add((uri_patient, hrt["hasExerciseProtocol"], Literal("McHenry", datatype=XSD["string"])))
                elif row["proto"] == 4:
                    rdf.add((uri_patient, hrt["hasExerciseProtocol"], Literal("FastBalke", datatype=XSD["string"])))
                elif row["proto"] == 5:
                    rdf.add((uri_patient, hrt["hasExerciseProtocol"], Literal("Balke", datatype=XSD["string"])))
                elif row["proto"] == 6:
                    rdf.add((uri_patient, hrt["hasExerciseProtocol"], Literal("Noughton", datatype=XSD["string"])))
                elif row["proto"] == 7:
                    rdf.add((uri_patient, hrt["hasExerciseProtocol"], Literal("Bike150kpa/min", datatype=XSD["string"])))
                elif row["proto"] == 8:
                    rdf.add((uri_patient, hrt["hasExerciseProtocol"], Literal("Bike125kpa/min", datatype=XSD["string"])))
                elif row["proto"] == 9:
                    rdf.add((uri_patient, hrt["hasExerciseProtocol"], Literal("Bike100kpa/min", datatype=XSD["string"])))
                elif row["proto"] == 10:
                    rdf.add((uri_patient, hrt["hasExerciseProtocol"], Literal("Bike75kpa/min", datatype=XSD["string"])))
                elif row["proto"] == 11:
                    rdf.add((uri_patient, hrt["hasExerciseProtocol"], Literal("Bike50kpa/min", datatype=XSD["string"])))
                else:
                    rdf.add((uri_patient, hrt["hasExerciseProtocol"], Literal("ArmErgometer", datatype=XSD["string"])))

            # 2.Create patient ECG Reading instance
            uri_ecg = URIRef(hrt + "ecg_patient_" + str(int(row['id'])))
            rdf.add((uri_ecg, RDF["type"], hrt["ExerciseECGReading"]))
            # 3.Create ECG Reading Heart Measurement instance
            uri_hmm = URIRef(hrt + "heart_ecg_patient_" + str(int(row['id'])))
            rdf.add((uri_hmm, RDF["type"], hrt["HeartMeasurements"]))
            # 4.Create Medical Used during Ecercise instance
            uri_med = URIRef(hrt + "medication_ecg_patient_" + str(int(row['id'])))
            rdf.add((uri_med, RDF["type"], hrt["MedicationDuringExercise"]))

            # 3.Link the ECG and the Heart Measurement obtained

            # REMARK!!: The check for 'value == value' is made to remove nan values

            # Add ECG reading data properties
            if row["thaldur"] is not None and row["thaldur"] == row["thaldur"]:
                rdf.add((uri_ecg, hrt["hasDuration"], Literal(row["thaldur"], datatype=XSD["float"])))
            if row["exang"] is not None and row["exang"] == row["exang"]:
                if int(row["exang"]) == 1:
                    rdf.add((uri_ecg, hrt["hasExerciseInducedAngina"], Literal("true", datatype=XSD["boolean"])))
                else:
                    rdf.add((uri_ecg, hrt["hasExerciseInducedAngina"], Literal("false", datatype=XSD["boolean"])))
            if row["xhypo"] is not None and row["xhypo"] == row["xhypo"]:
                if int(row["xhypo"]) == 1:
                    rdf.add((uri_ecg, hrt["hasExerciseInduceHypotension"], Literal("true", datatype=XSD["boolean"])))
                else:
                    rdf.add((uri_ecg, hrt["hasExerciseInduceHypotension"], Literal("false", datatype=XSD["boolean"])))
            if row["oldpeak"] is not None and row["oldpeak"] == row["oldpeak"]:
                rdf.add((uri_ecg, hrt["hasExerciseInducedSTDepression"], Literal(row["oldpeak"], datatype=XSD["float"])))
            if row["ekgmo"] is not None and row["ekgmo"] == row["ekgmo"]:
                rdf.add((uri_ecg, hrt["hasMonthReading"], Literal(int(row["ekgmo"]), datatype=XSD["integer"])))
            if row["ekgday"] is not None and row["ekgday"] == row["ekgday"]:
                rdf.add((uri_ecg, hrt["hasDayReading"], Literal(int(row["ekgday"]), datatype=XSD["integer"])))
            if row["ekgyr"] is not None and row["ekgyr"] == row["ekgyr"]:
                rdf.add((uri_ecg, hrt["hasYearReading"], Literal(int(row["ekgyr"]), datatype=XSD["integer"])))
            if row["met"] is not None and row["met"] == row["met"]:
                rdf.add((uri_ecg, hrt["hasMETSTestScore"], Literal(int(row["met"]), datatype=XSD["integer"])))

            # Add Heart Measurements data properties
            if row["thalach"] is not None and row["thalach"] == row["thalach"]:
                rdf.add((uri_hmm, hrt["hasMaximumHeartRateAchieved"], Literal(int(row["thalach"]), datatype=XSD["integer"])))
            if row["thalrest"] is not None and row["thalrest"] == row["thalrest"]:
                rdf.add((uri_hmm, hrt["hasRestingHeartRateAchieved"], Literal(int(row["thalrest"]), datatype=XSD["integer"])))
            if row["tpeakbps"] is not None and row["tpeakbps"] == row["tpeakbps"]:
                rdf.add((uri_hmm, hrt["hasPeakBloodPressure1Achieved"], Literal(int(row["tpeakbps"]), datatype=XSD["integer"])))
            if row["tpeakbpd"] is not None and row["tpeakbpd"] == row["tpeakbpd"]:
                rdf.add((uri_hmm, hrt["hasPeakBloodPressure2Achieved"], Literal(int(row["tpeakbpd"]), datatype=XSD["integer"])))
            if row["trestbpd"] is not None and row["trestbpd"] == row["trestbpd"]:
                rdf.add((uri_hmm, hrt["hasRestingBloodPressureAchieved"], Literal(int(row["trestbpd"]), datatype=XSD["integer"])))
            if row["rldv5e"] is not None and row["rldv5e"] == row["rldv5e"]:
                rdf.add((uri_hmm, hrt["hasHeightAtPeakExerciseAchieved"], Literal(int(row["rldv5e"]), datatype=XSD["integer"])))

            # Add Medication during exercise data properties
            if row["dig"] is not None and row["dig"] == row["dig"]:
                if row["dig"] == float(1):
                    rdf.add((uri_med, hrt["usedDigitalis"], Literal("true", datatype=XSD["boolean"])))
                else:
                     rdf.add((uri_med, hrt["usedDigitalis"], Literal("false", datatype=XSD["boolean"])))
            if row["prop"] is not None and row["prop"] == row["prop"]:
                if row["prop"] == float(1):
                    rdf.add((uri_med, hrt["usedBetablocker"], Literal("true", datatype=XSD["boolean"])))
                else:
                    rdf.add((uri_med, hrt["usedBetablocker"], Literal("false", datatype=XSD["boolean"])))
            if row["nitr"] is not None and row["nitr"] == row["nitr"]:
                if row["nitr"] == float(1):
                    rdf.add((uri_med,hrt["usedNitrates"],Literal("true", datatype=XSD["boolean"])))
                else:
                    rdf.add((uri_med,hrt["usedNitrates"],Literal("false", datatype=XSD["boolean"])))
            if row["pro"] is not None and row["pro"] == row["pro"]:
                if row["pro"] == float(1):
                    rdf.add((uri_med, hrt["usedCalciumChannelBlocker"], Literal("true", datatype=XSD["boolean"])))
                else:
                    rdf.add((uri_med, hrt["usedCalciumChannelBlocker"], Literal("false", datatype=XSD["boolean"])))
            if row["diuretic"] is not None and row["diuretic"] == row["diuretic"]:
                if row["diuretic"] == float(1):
                    rdf.add((uri_med, hrt["usedDiuretics"], Literal("true", datatype=XSD["boolean"])))
                else:
                    rdf.add((uri_med, hrt["usedDiuretics"], Literal("false", datatype=XSD["boolean"])))


            # Create patient Coronary Angiograms Diagnosis instance
            uri_ca = URIRef(hrt + "coronary_patient_" + '_' +str(int(row['id'])))
            rdf.add((uri_ca, RDF["type"], hrt["CoronaryAngiogramsDiagnosis"]))

            # Add Coronary Angiograms Diagnosis data properties
            if row["cmo"] is not None and row["cmo"] == row["cmo"]:
                rdf.add((uri_ca, hrt["hasMonthCardiacCath"], Literal(int(row["cmo"]), datatype=XSD["integer"])))
            if row["cday"] is not None and row["cday"] == row["cday"]:
                rdf.add((uri_ca, hrt["hasDayCardiacCath"], Literal(int(row["cday"]), datatype=XSD["integer"])))
            if row["cyr"] is not None and row["cyr"] == row["cyr"]:
                rdf.add((uri_ca, hrt["hasYearCardiacCath"], Literal(int(row["cyr"]), datatype=XSD["integer"])))
            if row["num"] is not None and row["num"] == row["num"]:
                rdf.add((uri_ca, hrt["hasHeartDiseaseDiagnosis"], Literal(int(row["num"]), datatype=XSD["integer"])))

            # Create patient Blood Vessels Diagnosis
            uri_bv = URIRef(hrt + "vessels_patient" + str(int(row['id'])))
            rdf.add((uri_bv, RDF["type"], hrt["BloodVesselsDiagnosis"]))

            # Add Coronary Angiograms Diagnosis data properties
            if row["lmt"] is not None and row["lmt"] == row["lmt"]:
                rdf.add((uri_bv, hrt["hasLeftMainTruck"], Literal(int(row["lmt"]), datatype=XSD["integer"])))
            if row["ladprox"] is not None and row["ladprox"] == row["ladprox"]:
                rdf.add((uri_bv, hrt["hasProximalLeftAnteriorDescendingArtery"], Literal(int(row["ladprox"]), datatype=XSD["integer"])))
            if row["laddist"] is not None and row["laddist"] == row["laddist"]:
                rdf.add((uri_bv, hrt["hasDistalLeftAnteriorDescendingArtery"], Literal(int(row["laddist"]), datatype=XSD["integer"])))
            if row["cxmain"] is not None and row["cxmain"] == row["cxmain"]:
                rdf.add((uri_bv, hrt["hasCircumflex"], Literal(int(row["cxmain"]), datatype=XSD["integer"])))
            if row["rcaprox"] is not None and row["rcaprox"] == row["rcaprox"]:
                rdf.add((uri_bv, hrt["hasProximalRightAnteriorDescendingArtery"], Literal(int(row["rcaprox"]), datatype=XSD["integer"])))
            if row["rcadist"] is not None and row["rcadist"] == row["rcadist"]:
                rdf.add((uri_bv, hrt["hasDistalRightAnteriorDescendingArtery"], Literal(int(row["rcadist"]), datatype=XSD["integer"])))

            # Object properties
            rdf.add((uri_patient, hrt["hasExerciseECGReading"], uri_ecg))
            rdf.add((uri_patient, hrt["hasCoronaryAngiogramsDiagnosis"], uri_ca))
            rdf.add((uri_patient, hrt["hasBloodVesselsDiagnosis"], uri_bv))
            rdf.add((uri_ecg, hrt["obtainedHeartMeasurements"], uri_hmm))
            rdf.add((uri_ecg, hrt["employedMedication"], uri_med))

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
