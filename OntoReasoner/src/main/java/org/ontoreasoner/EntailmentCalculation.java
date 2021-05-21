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

import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.util.Set;

public class EntailmentCalculation {

    public static void main(String[] args){

        // ###### LOADING THE ONTOLOGY ######

        // Initialization
        // Ontology Manager
        OWLOntologyManager manager = OWLManager.createOWLOntologyManager();
        // File object
        File flights_file = new File("/home/jdiaz/Knowledge bases TL/ExplicabilityOntologyBasedML/Onto/FlightOntology.owl");
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
            /*
            // Default Prefix Manaager
            DefaultPrefixManager pm = new DefaultPrefixManager(null,null,"http://www.cs.ox.ac.uk/isg/krr/ontologies/FlightOntology-1#");

            // Get all the flights
            OWLDataFactory fac = manager.getOWLDataFactory();
            //Define the class
            OWLClass flights = fac.getOWLClass(IRI.create(pm.getDefaultPrefix(), "Flights"));
            // Get Individuals for this class
            NodeSet<OWLNamedIndividual> individualNodeSet = reasoner.getInstances(flights, false);
            // Transform NodeSet into a Set
            Set<OWLNamedIndividual> individualSet = individualNodeSet.getFlattened();

            for (OWLNamedIndividual individualFlights : individualSet) {
                System.out.println("Individual name: " + individualFlights);
            }

             */

        } catch (OWLOntologyCreationException e) {
            e.printStackTrace();
        }


    }
}
