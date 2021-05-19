import numpy as np
import pandas as pd

from math import nan
from rdflib import Graph, Literal, BNode, Namespace, URIRef
from rdflib.namespace import RDF, XSD
from tqdm import tqdm

ontology_file = 'FlightOntology.owl'

folder = '/home/jdiaz/Knowledge bases TL/Replica/results'

out_file = '../Example'

csv_file_2010 = 'data/FlightData/trydata.csv'

def addMeteo(meteo_csv_file):
    dataframe = pd.read_csv(meteo_csv_file)
    for index, row in tqdm(dataframe.iterrows()):
        uri_meteo = URIRef(flt + 'meteo' + '_ATL_' + row['hour'])
        rdf.add((uri_meteo, RDF['type'], flt['Weather']))
        rdf.add((uri_meteo, flt['hasCloudCover'], Literal(row['cloudCover'], datatype=XSD['float'])))
        rdf.add((uri_meteo, flt['hasDewPoint'], Literal(row['dewPoint'], datatype=XSD['float'])))
        rdf.add((uri_meteo, flt['hasHumidity'], Literal(row['humidity'], datatype=XSD['float'])))
        rdf.add((uri_meteo, flt['hasPrecipType'], Literal(row['precipType'], datatype=XSD['string'])))
        rdf.add((uri_meteo, flt['hasPressure'], Literal(row['pressure'], datatype=XSD['float'])))
        rdf.add((uri_meteo, flt['hasSummary'], Literal(row['summary'], datatype=XSD['string'])))
        rdf.add((uri_meteo, flt['hasTemperature'], Literal(row['temperature'], datatype=XSD['float'])))
        rdf.add((uri_meteo, flt['hasVisibility'], Literal(row['visibility'], datatype=XSD['float'])))
        rdf.add((uri_meteo, flt['hasWindBearing'], Literal(row['windBearing'], datatype=XSD['float'])))
        rdf.add((uri_meteo, flt['hasWindSpeed'], Literal(row['windSpeed'], datatype=XSD['float'])))

def add_data_properties(dep_csv_file):
    dataframe = pd.read_csv(dep_csv_file)
    for index, row in tqdm(dataframe.iterrows()):

        # Check that the flight has not been cancelled
        if row['CANCELLED'] == 0.0:

            # Add URI Ref for departure
            uri_dep = URIRef(flt + 'dep' + '_2010_' + str(row['FL_DATE']) + '_' + str(row['OP_CARRIER_FL_NUM']))
            # Map to Departure class
            rdf.add((uri_dep, RDF['type'], flt['Departure']))

            # Add Data Properties
            rdf.add((uri_dep, flt['hasArrDelay'], Literal(row['ARR_DELAY'], datatype=XSD['float'])))
            rdf.add((uri_dep, flt['hasArrTime'], Literal(row['ARR_TIME'], datatype=XSD['string'])))

            rdf.add((uri_dep, flt['hasCRSArrTime'], Literal(row['CRS_ARR_TIME'], datatype=XSD['string'])))
            rdf.add((uri_dep, flt['hasCRSDepTime'], Literal(row['CRS_DEP_TIME'], datatype=XSD['string'])))
            rdf.add((uri_dep, flt['hasDepTime'], Literal(row['DEP_TIME'], datatype=XSD['string'])))
            rdf.add((uri_dep, flt['hasDistance'], Literal(row['DISTANCE'], datatype=XSD['float'])))
            rdf.add((uri_dep, flt['hasFlightDate'], Literal(row['FL_DATE'], datatype=XSD['string'])))

            # The check for 'value == value' is made to remove nan values
            if row['DEP_DELAY'] is not None and row['DEP_DELAY'] == row['DEP_DELAY']:
                rdf.add((uri_dep, flt['hasDepDelay'], Literal(row['DEP_DELAY'], datatype=XSD['float'])))
            if row['CARRIER_DELAY'] is not None and row['CARRIER_DELAY'] == row['CARRIER_DELAY']:
                rdf.add((uri_dep, flt['hasCarrierDelay'], Literal(row['CARRIER_DELAY'], datatype=XSD['float'])))
            if row['LATE_AIRCRAFT_DELAY'] is not None and row['LATE_AIRCRAFT_DELAY'] == row['LATE_AIRCRAFT_DELAY']:
                rdf.add((uri_dep, flt['hasLateAircraftDelay'], Literal(row['LATE_AIRCRAFT_DELAY'], datatype=XSD['float'])))
            if row['NAS_DELAY'] is not None and row['NAS_DELAY'] == row['NAS_DELAY']:
                rdf.add((uri_dep, flt['hasNASDelay'], Literal(row['NAS_DELAY'], datatype=XSD['float'])))
            if row['SECURITY_DELAY'] is not None and row['SECURITY_DELAY'] == row['SECURITY_DELAY']:
                rdf.add((uri_dep, flt['hasSecurityDelay'], Literal(row['SECURITY_DELAY'], datatype=XSD['float'])))
            if row['WEATHER_DELAY'] is not None and row['WEATHER_DELAY'] == row['WEATHER_DELAY']:
                rdf.add((uri_dep, flt['hasWeatherDelay'], Literal(row['WEATHER_DELAY'], datatype=XSD['float'])))
        else:
            # Add URI Ref for departure
            uri_cancelled = URIRef(flt + 'cancelled' + '_2010_' + str(row['FL_DATE']) + '_' + str(row['OP_CARRIER_FL_NUM']))
            # Map to Cancelled class
            rdf.add((uri_cancelled, RDF['type'], flt['Cancelled']))

            # Add Data Properties
            rdf.add((uri_cancelled, flt['hasCancelCode'], Literal(row['CANCELLATION_CODE'], datatype=XSD['string'])))
            rdf.add((uri_cancelled, flt['hasCRSArrTime'], Literal(row['CRS_ARR_TIME'], datatype=XSD['string'])))
            rdf.add((uri_cancelled, flt['hasCRSDepTime'], Literal(row['CRS_DEP_TIME'], datatype=XSD['string'])))
            rdf.add((uri_cancelled, flt['hasDepTime'], Literal(row['DEP_TIME'], datatype=XSD['string'])))
            rdf.add((uri_cancelled, flt['hasDistance'], Literal(row['DISTANCE'], datatype=XSD['float'])))
            rdf.add((uri_cancelled, flt['hasFlightDate'], Literal(row['FL_DATE'], datatype=XSD['string'])))

#def add_flight

def add_object_properties(dep_csv_file):
    dataframe = pd.read_csv(dep_csv_file)
    for index, row in dataframe.iterrows():
        # Extract Carrier, Origin, Destination
        car = row['OP_CARRIER']
        ori = row['ORIGIN']
        dest = row['DEST']
        flight_num

        # Add Object Properties
        #rdf.add(uri_dep, flt['hasCarrier'], flt[car])
        #rdf.add(uri_dep, flt['hasDest'], flt[dest])
        #rdf.add(uri_dep, flt['hasOri'], flt[ori])
        # rdf.add(uri_dep, flt['hasFlight'], flt[ori])


def addTarget(target_csv_file):
    dataframe = pd.read_csv(target_csv_file)
    for index, row in dataframe.iterrows():
        uri_target = URIRef(flt + '_' + row['Carrier'] + '_' + row['FlightNum'])
        rdf.add((uri_target, RDF['type'], flt['Carrier']))
        rdf.add((uri_target, flt['hasDest']))

if __name__ == '__main__':

    # Set up namespace used
    flt = Namespace('http://www.cs.ox.ac.uk/isg/krr/ontologies/FlightOntology-1#')

    # Generate graph
    rdf = Graph()

    # Add ontology to file
    rdf.parse(ontology_file,format='xml')

    # Bind namespace to prefix
    rdf.bind('flt', flt)

    # Call function
    add_data_properties(csv_file_2010)




    print(f"Saved file {out_file}")
    with open(out_file + '.rdf', 'w+') as f:
        f.write(rdf.serialize(format='ntriples').decode('utf-8'))



