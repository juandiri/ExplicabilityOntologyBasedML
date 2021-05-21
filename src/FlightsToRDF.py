import os.path
import pandas as pd

from rdflib import Graph, Literal, BNode, Namespace, URIRef
from rdflib.namespace import RDF, XSD
from tqdm import tqdm

ontology_file = '../Onto/FlightOntology.owl'

folder = '../Onto/'

out_file = '../SampleRDFInsertion'

csv_file_2010 = '../SampleData/SampleFlights.csv'

meteo_file = '../SampleData/ATL.csv'

airports_file = '../SampleData/airports.csv'

def add_meteo(meteo_csv_file):

    with open(meteo_csv_file, 'r') as f:
        [file_name, f_format] = os.path.basename(f.name).split('.')

    dataframe = pd.read_csv(meteo_csv_file)
    for index, row in tqdm(dataframe.iterrows()):
        # Since the file name containing weather information has the name of the Airport
        # Search for the airport in the ontology
        uri_airport = flt[file_name]

        # Create instance for the weather
        uri_meteo = URIRef(flt + 'meteo_' + file_name + '_' +row['hour'])
        rdf.add((uri_meteo, RDF['type'], flt['Weather']))

        # Add Object Propertities
        rdf.add((uri_airport, flt['hasWeather'], uri_meteo))

        # Add Data Propertities
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

def add_departure(dep_csv_file):
    dataframe = pd.read_csv(dep_csv_file)
    for index, row in tqdm(dataframe.iterrows()):
        # Extract Carrier, Origin, Destination
        carrier = row['OP_CARRIER']
        origin = row['ORIGIN']
        destination = row['DEST']
        flight_num = row['OP_CARRIER_FL_NUM']

        # Check that the flight has not been cancelled
        if row['CANCELLED'] == 0.0:
            # Add URI Ref for departure
            uri_dep = URIRef(flt + 'dep_' + str(row['FL_DATE']) + '_' + str(row['OP_CARRIER_FL_NUM']))
            # Map to Departure class
            rdf.add((uri_dep, RDF['type'], flt['Departure']))
        else:
            # Add URI Ref for Cancelled Departure
            uri_dep = URIRef(flt + 'cancelled' + '_' + str(row['FL_DATE']) + '_' + str(row['OP_CARRIER_FL_NUM']))
            # Map to Cancelled class
            rdf.add((uri_dep, RDF['type'], flt['Cancelled']))

        # Add URI Ref for flight number
        uri_flight = URIRef(flt['Flight'] + str(flight_num))
        rdf.add((uri_flight, RDF['type'], flt['Flight']))

        # Map to the URI defined in the ontology for each carrier, origin and destination airport
        uri_car = flt[carrier]
        rdf.add((uri_car, RDF['type'], flt['Carrier']))
        uri_ori = flt[origin]
        rdf.add((uri_ori, RDF['type'], flt['Airport']))
        uri_dest = flt[destination]
        rdf.add((uri_dest, RDF['type'], flt['Airport']))

        # Add Object Propertities

        rdf.add((uri_dep, flt['hasCarrier'], uri_car))
        rdf.add((uri_dep, flt['hasDest'], uri_dest))
        rdf.add((uri_dep, flt['hasFlight'], uri_flight))
        rdf.add((uri_dep, flt['hasOrigin'], uri_ori))

        # Add Data Properties

        # The check for 'value == value' is made to remove nan values
        if row['ARR_DELAY'] is not None and row['ARR_DELAY'] == row['ARR_DELAY']:
            rdf.add((uri_dep, flt['hasArrDelay'], Literal(row['ARR_DELAY'], datatype=XSD['float'])))
        if row['ARR_TIME'] is not None and row['ARR_TIME'] == row['ARR_TIME']:
            rdf.add((uri_dep, flt['hasArrTime'], Literal(row['ARR_TIME'], datatype=XSD['string'])))
        if row['CRS_ARR_TIME'] is not None and row['CRS_ARR_TIME'] == row['CRS_ARR_TIME']:
            rdf.add((uri_dep, flt['hasCRSArrTime'], Literal(row['CRS_ARR_TIME'], datatype=XSD['string'])))
        if row['CRS_DEP_TIME'] is not None and row['CRS_DEP_TIME'] == row['CRS_DEP_TIME']:
            rdf.add((uri_dep, flt['hasCRSDepTime'], Literal(row['CRS_DEP_TIME'], datatype=XSD['string'])))
        if row['DEP_TIME'] is not None and row['DEP_TIME'] == row['DEP_TIME']:
            rdf.add((uri_dep, flt['hasDepTime'], Literal(row['DEP_TIME'], datatype=XSD['string'])))
        if row['DISTANCE'] is not None and row['DISTANCE'] == row['DISTANCE']:
            rdf.add((uri_dep, flt['hasDistance'], Literal(row['DISTANCE'], datatype=XSD['float'])))
        if row['DEP_DELAY'] is not None and row['DEP_DELAY'] == row['DEP_DELAY']:
            rdf.add((uri_dep, flt['hasFlightDate'], Literal(row['FL_DATE'], datatype=XSD['string'])))
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
        if row['CANCELLATION_CODE'] is not None and row['CANCELLATION_CODE'] == row['CANCELLATION_CODE']:
            rdf.add((uri_dep, flt['hasCancelCode'], Literal(row['CANCELLATION_CODE'], datatype=XSD['string'])))

def add_locations(airport_csv_file):

    dataframe = pd.read_csv(airport_csv_file)

    for index, row in tqdm(dataframe.iterrows()):

        # Select the airport and the city, state it is located in
        airport = row['IATA_CODE'].replace(' ', '_')
        city = row['CITY'].replace(' ', '_')
        state = row['STATE'].replace(' ', '_')

        # Add a new instance of airport in case the airport is not in the ontolgy
        uri_airport = URIRef(flt + airport)
        rdf.add((uri_airport, RDF['type'], flt['Airport']))

        # Add new city
        uri_city = URIRef(flt + 'city_' + city + '_' + state)
        rdf.add((uri_city, RDF['type'], flt['City']))

        # Add new state
        uri_state = URIRef(flt + 'state_'+state)
        rdf.add((uri_state, RDF['type'], flt['State']))

        # Add Object Properties
        rdf.add((uri_airport, flt['locatedIn'], uri_city))
        rdf.add((uri_airport, flt['serveCity'], uri_city))
        rdf.add((uri_city, flt['locatedIn'], uri_state))

        # Add Data Propertities
        rdf.add((uri_airport, flt['hasLocationName'], Literal(row['AIRPORT'], datatype=XSD['string'])))
        rdf.add((uri_city, flt['hasLocationName'], Literal(row['CITY'], datatype=XSD['string'])))
        rdf.add((uri_state, flt['hasLocationName'], Literal(row['STATE'], datatype=XSD['string'])))

if __name__ == '__main__':

    # Set up namespace used
    flt = Namespace('http://www.cs.ox.ac.uk/isg/krr/ontologies/FlightOntology-1#')

    # Generate graph
    rdf = Graph()

    # Add ontology to file
    rdf.parse(ontology_file,format='xml')

    # Bind namespace to prefix
    rdf.bind('flt', flt)

    # Call function to add departure instances to the ontology
    add_departure(csv_file_2010)

    # Call function to add meteeo instances to the ontology
    add_meteo(meteo_file)

    # Call function to add departure instances to the ontology
    add_locations(airports_file)


    print(f"Saved file {out_file}")
    with open(out_file + '.xml', 'w+') as f:
        f.write(rdf.serialize(format='xml').decode('utf-8'))




