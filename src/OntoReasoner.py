import owlready2

from owlready2 import *

onto_file = '../SampleRDFInsertion.rdf'

onto = get_ontology(onto_file).load()

with onto: sync_reasoner()
onto.save("test_t1.owl")