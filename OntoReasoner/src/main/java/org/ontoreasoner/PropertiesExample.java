package org.ontoreasoner;
import org.checkerframework.checker.units.qual.A;
import org.eclipse.rdf4j.model.vocabulary.OWL;
import org.junit.Before;
import org.junit.Rule;
import org.junit.Test;
import org.junit.rules.TestName;
import org.semanticweb.HermiT.Reasoner;
import org.semanticweb.HermiT.ReasonerFactory;
import org.semanticweb.owlapi.reasoner.OWLReasoner;
import org.semanticweb.owlapi.apibinding.OWLManager;
import org.semanticweb.owlapi.model.*;
import org.semanticweb.owlapi.model.parameters.Imports;
import org.semanticweb.owlapi.reasoner.*;
import org.semanticweb.owlapi.search.EntitySearcher;
import org.semanticweb.owlapi.util.DefaultPrefixManager;
import org.semanticweb.owlapi.vocab.OWL2Datatype;
import org.testng.annotations.BeforeClass;
import uk.ac.manchester.cs.owl.owlapi.OWLDataPropertyImpl;
import uk.ac.manchester.cs.owl.owlapi.OWLObjectPropertyImpl;

import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.util.Collection;
import java.util.HashSet;
import java.util.Set;
import java.util.stream.Collectors;

public class PropertiesExample {

    public static void main(String[] args){

        // ###### LOADING THE ONTOLOGY ######

        // Initialization
        // Ontology Manager
        OWLOntologyManager manager = OWLManager.createOWLOntologyManager();
        // File object
        File flights_file = new File("/home/jdiaz/KnowledgeBasesTL/ExplicabilityOntologyBasedML/Onto/FlightOntology.owl");
        // Prepare OWL Ontology classes to store in memory the ontology
        OWLOntology localFlights;

        // Load the ontology
        try {
            localFlights = manager.loadOntologyFromOntologyDocument(flights_file);
            // Get the identity of the ontology
            System.out.println("Loaded Ontology: " + localFlights.getOntologyID());
            IRI location = IRI.create("http://www.cs.ox.ac.uk/isg/krr/ontologies/FlightOntology-1#");
            System.out.println("\t from: " + location);

            // Get and configure HermiT reasoner
            OWLReasonerFactory reasonerFactory = new ReasonerFactory();
            // Configure console process monitor
            ConsoleProgressMonitor progressMonitor = new ConsoleProgressMonitor();
            // Load default configuration for the reasoner
            OWLReasonerConfiguration config = new SimpleConfiguration(progressMonitor);

            // Create Reasoner Instance, classify the ontology and compute inferences
            OWLReasoner reasoner = reasonerFactory.createReasoner(localFlights, config);
            // Compute default inferences (Compute the possible reasonings)
            reasoner.precomputeInferences(InferenceType.values());
            // Default Prefix Manager
            DefaultPrefixManager pm = new DefaultPrefixManager(null,null,"http://www.cs.ox.ac.uk/isg/krr/ontologies/FlightOntology-1#");

            // Get all the airports
            OWLDataFactory fac = manager.getOWLDataFactory();
            // Create IRI for the class "Airport"
            OWLClass airports = fac.getOWLClass(IRI.create(pm.getDefaultPrefix(), "Airport"));
            // Get Individuals for this class
            NodeSet<OWLNamedIndividual> airportsNodeSet = reasoner.getInstances(airports, false);
            // Transform NodeSet into a Set
            Set<OWLNamedIndividual> airportsSet = airportsNodeSet.getFlattened();
            // Print individuals
            for (OWLNamedIndividual airport : airportsSet) {
                System.out.println("Airport name" + pm.getShortForm(airport));

                // Get Object Properties
                OWLObjectPropertyImpl op = new OWLObjectPropertyImpl(IRI.create(pm.getDefaultPrefix(), "hasWeather"));
                Set<OWLIndividual> weathers = new HashSet<>(EntitySearcher.getObjectPropertyValues(airport, op, localFlights).collect(Collectors.toSet()));

                for (OWLIndividual weather : weathers) {
                    System.out.println("Weather summary" + pm.getShortForm((OWLEntity) weather));
                    //Get Data Properties
                    OWLDataProperty weatherSummary = new OWLDataPropertyImpl(IRI.create(pm.getDefaultPrefix(), "hasSummary"));
                    System.out.println(EntitySearcher.getDataPropertyValues(weather, weatherSummary, localFlights));

                    // Get
                    OWLObjectPropertyImpl op1 = new OWLObjectPropertyImpl(IRI.create(pm.getDefaultPrefix(), "serveCity"));
                    Set<OWLIndividual> servedCities = new HashSet<>(EntitySearcher.getObjectPropertyValues(airport, op1, localFlights).collect(Collectors.toSet()));

                    for (OWLIndividual city: servedCities) {
                        System.out.println("City name" + pm.getShortForm((OWLEntity) city));
                    }
                }
            }
        } catch (OWLOntologyCreationException e) {
            e.printStackTrace();
        }


    }
}
