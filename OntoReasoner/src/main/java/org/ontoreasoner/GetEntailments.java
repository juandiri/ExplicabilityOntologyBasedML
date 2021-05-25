package org.ontoreasoner;

import org.eclipse.rdf4j.model.vocabulary.OWL;
import org.semanticweb.HermiT.Reasoner;
import org.semanticweb.HermiT.ReasonerFactory;
import org.semanticweb.owlapi.apibinding.OWLManager;
import org.semanticweb.owlapi.model.*;
import org.semanticweb.owlapi.reasoner.*;
import org.semanticweb.owlapi.util.DefaultPrefixManager;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;

public class GetEntailments {

    private OWLOntologyManager manager = null;
    private OWLDataFactory factory = null;
    private OWLOntology localOnto = null;
    private OWLDatatype t_int = null;
    private OWLDatatype t_string = null;
    private OWLDatatype t_float = null;
    private String ontIRI = null;
    private PrefixManager pm = null;
    private String HOME_DIR = null;
    private String dom_dir = null;
    private File snp_f = null;

    GetEntailments(String ontology_filepath, String onto_iri) throws OWLOntologyCreationException {
        // Load the ontology
        OWLOntology localOnto = loadOntology(ontology_filepath);

    }

    public OWLOntology loadOntology(String ontology_filepath) throws OWLOntologyCreationException{
        // Ontology Manager
        OWLOntologyManager manager = OWLManager.createOWLOntologyManager();
        // Create File object for the ontology
        File ontology_file = new File(ontology_filepath);
        // Prepare OWL Ontology classes to store in memory
        OWLOntology localOntology;
        // Load Ontology from file
        return localOntology = manager.loadOntologyFromOntologyDocument(ontology_file);
    }

    public ArrayList<String> getEntClosure() {
        ArrayList<String> G = new ArrayList<>();
        // Get and configure HermiT reasoner
        OWLReasonerFactory reasonerFactory = new ReasonerFactory();
        // Configure console process monitor
        ConsoleProgressMonitor progressMonitor = new ConsoleProgressMonitor();
        // Load default configuration for the reasoner
        OWLReasonerConfiguration config = new SimpleConfiguration(progressMonitor);

        // Create Reasoner Instance, classify the ontology and compute inferences
        OWLReasoner reasoner = reasonerFactory.createReasoner(localOnto, config);

        OWLNamedIndividual[] S = localOnto.individualsInSignature().toArray(OWLNamedIndividual[]::new);
        OWLObjectProperty[] OP = localOnto.objectPropertiesInSignature().toArray(OWLObjectProperty[]::new);

        for (OWLNamedIndividual individual:S) {
            for (OWLObjectProperty objectProperty: OP) {
                if (objectProperty.getIRI().equals("topObjectProperty")){
                    continue;
                }
                NodeSet<OWLNamedIndividual> individualValues = reasoner.getObjectPropertyValues(individual,objectProperty);
                OWLNamedIndividual[] O = individualValues.entities().toArray(OWLNamedIndividual[]::new);
                if (O.length > 0){
                    for(OWLNamedIndividual o:O){
                        G.add(String.format("%s,%s,%s", individual.toStringID().substring(ontIRI.length()),
                                objectProperty.getIRI().getFragment(),o.getIRI().getFragment()));
                    }
                }
            }
        }
        for (OWLClass c : localOnto.classesInSignature().toArray(OWLClass[]::new)){
            NodeSet<OWLNamedIndividual> individualsSet = reasoner.getInstances(c,false);
            OWLNamedIndividual[] individualsArray = individualsSet.entities().toArray(OWLNamedIndividual[]::new);
            for (OWLNamedIndividual individual: individualsArray) {
                G.add(String.format("%s,%s", c.getIRI().getFragment(), individual.getIRI().getFragment()));
            }
        }

        return G;
    }

    private static ArrayList<ArrayList<String>> getEntClosures(String dom, String e_f) throws OWLOntologyCreationException, IOException {
        File ent_num_f = new File(e_f, String.format("%s_ent_num.csv", dom));
        ArrayList<String> snp_ids = getSnpIDs(dom);
        System.out.println("Snapshot size: " + snp_ids.size());
        ArrayList<ArrayList<String>> Gs = new ArrayList<>();
        FileWriter writer = new FileWriter(ent_num_f.getPath());
        for (int i = 0; i < snp_ids.size(); i++) {
            Snapshot snp = new Snapshot(SNP, dom, snp_ids.get(i), HOME_DIR, ontIRI);
            ArrayList<String> G = snp.getEntClosure();
            Gs.add(G);
            writer.write(String.format("%s,%d\n", snp_ids.get(i), G.size()));
            if (i % 100 == 0) {
                System.out.printf("%d: %s, %d \n", i, snp_ids.get(i), G.size());
            }
        }
        writer.close();
        return Gs;
    }

}
