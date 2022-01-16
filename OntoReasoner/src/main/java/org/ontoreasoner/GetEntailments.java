package org.ontoreasoner;

import org.eclipse.rdf4j.model.vocabulary.OWL;
import org.semanticweb.HermiT.Reasoner;
import org.semanticweb.HermiT.ReasonerFactory;
import org.semanticweb.owlapi.apibinding.OWLManager;
import org.semanticweb.owlapi.model.*;
import org.semanticweb.owlapi.reasoner.*;
import org.semanticweb.owlapi.search.EntitySearcher;
import org.semanticweb.owlapi.util.DefaultPrefixManager;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Set;

public class GetEntailments {

    // Directory where the ontologies are contained
    private static String ONTO_DIR = "/home/juandiri/TFM/TFM/RDFInsertions/3";
    // IRI of the ontology
    private static String ontoIRI = "http://www.semanticweb.org/juandiri/ontologies/2021/9/untitled-ontology-7#";
    // Output name according to the query performed
    public static String output_name;
    private static String ENT = "Entailments";
    public static OWLOntology localOnto;
    static OWLReasoner reasoner;
    static OWLReasonerFactory reasonerFactory;
    static OWLOntologyManager ontologyManager;
    static DefaultPrefixManager pm;
    static ArrayList<String> domains = new ArrayList<String>();



    public static void main(String args[]) throws OWLOntologyCreationException, IOException {

        // Adding the different domains
        domains.add("Cleveland");
        domains.add("Hungary");
        domains.add("LongBeach");
        domains.add("Switzerland");

        if (args != null && args.length > 1) {
            ONTO_DIR = args[0];
        }

        // Create directory to store entailments
        File e_f = new File(ONTO_DIR, ENT);
        if (!e_f.exists()) {
            e_f.mkdir();
        }

        for(String dom: domains) {
            ArrayList<ArrayList<String>> Gs = getEntClosures(dom, e_f.getPath());

            // ArrayList to store the class and role entailments
            ArrayList<String> class_ents = new ArrayList<>();
            ArrayList<String> role_ents = new ArrayList<>();


            // For each entailment closure, add the class and role entailments
            for (ArrayList<String> G : Gs) {
                for (String g : G) {
                    if (g.split(",").length == 2 && !class_ents.contains(g)) {
                        class_ents.add(g);
                    }
                    if (g.split(",").length == 3 && !role_ents.contains(g)) {
                        role_ents.add(g);
                    }
                }
            }

            // Output files
            File class_ent_f = new File(e_f.getPath(), String.format("%s_class_ents.csv", dom));
            File role_ent_f = new File(e_f.getPath(), String.format("%s_role_ents.csv", dom));

            // Writing the class and roles entailments
            output_ents(class_ent_f, class_ents);
            output_ents(role_ent_f, role_ents);

            // Calculate the entailment importance
            System.out.println("Calculate entailment importance \n");
            HashMap<String, Float> imp = calImportance(Gs);

            // Calculate the effectiveness of the class and role entailments
            System.out.println("Calculate entailment effectiveness \n");
            ArrayList<String> ents = new ArrayList<>();
            ents.addAll(class_ents);
            ents.addAll(role_ents);
            HashMap<String, Float[]> eff = calEffectiveness(Gs, ents);

            // Write previous results into file
            File imp_f = new File(e_f.getPath(), String.format("%s_imp.csv", dom));
            FileWriter imp_writer = new FileWriter(imp_f.getPath());
            for (String g : imp.keySet()) {
                imp_writer.write(String.format("%s:%f\n", g, imp.get(g)));
            }
            imp_writer.close();

            File eff_f = new File(e_f.getPath(), String.format("%s_eff.csv", dom));
            FileWriter eff_writer = new FileWriter(eff_f.getPath());
            for (String g : eff.keySet()) {
                Float[] e = eff.get(g);
                eff_writer.write(String.format("%s:%f,%f,%f\n", g, e[0], e[1], e[2]));
                }
            }
        }


        // Calculating the set of entailments closures


    // Method that takes a File Path and Load the ontology and set needed variables
    // to perform the reasoning
    public static void loadOntology(String ontology_filepath) throws OWLOntologyCreationException{

        // Ontology Manager
        ontologyManager = OWLManager.createOWLOntologyManager();
        // Create File object for the ontology
        File ontology_file = new File(ontology_filepath);
        // Load Ontology from file
        localOnto = ontologyManager.loadOntologyFromOntologyDocument(ontology_file);
        // Load Onto IRI


        // Get and configure HermiT reasoner
        reasonerFactory = new ReasonerFactory();
        // Default Prefix Manager
        pm = new DefaultPrefixManager(null,null,"http://www.semanticweb.org/juandiri/ontologies/2021/9/untitled-ontology-7#");
    }

    // Method that takes and ontology an calculate its entailment closure
    public static ArrayList<String> getEntClosure(OWLOntology onto) {

        // Configure console process monitor
        ConsoleProgressMonitor progressMonitor = new ConsoleProgressMonitor();
        // Load default configuration for the reasoner
        OWLReasonerConfiguration config = new SimpleConfiguration(progressMonitor);

        // Create Reasoner Instance, classify the ontology and compute inferences
        reasoner = reasonerFactory.createReasoner(onto, config);

        // ArrayList to store entailments
        ArrayList<String> G = new ArrayList<>();

        //Get all the individuals which are referenced in the ontology
        OWLNamedIndividual[] S = onto.individualsInSignature().toArray(OWLNamedIndividual[]::new);
        //Get all the object properties which are referenced in the ontology
        OWLObjectProperty[] OP = onto.objectPropertiesInSignature().toArray(OWLObjectProperty[]::new);

        // Calculate the entailments for each individual with its object properties
        for (OWLNamedIndividual individual:S) {
            for (OWLObjectProperty objectProperty: OP) {
                if (objectProperty.getIRI().equals("topObjectProperty")){
                    continue;
                }
                // Reason the object property values for each individual and store them
                NodeSet<OWLNamedIndividual> individualValues = reasoner.getObjectPropertyValues(individual,objectProperty);
                OWLNamedIndividual[] O = individualValues.entities().toArray(OWLNamedIndividual[]::new);
                if (O.length > 0){
                    for(OWLNamedIndividual o:O){
                        G.add(String.format("%s,%s,%s",
                                individual
                                        .toStringID()
                                        .substring(ontoIRI.length()),
                                objectProperty
                                        .getIRI()
                                        .getFragment(),
                                o
                                        .getIRI()
                                        .getFragment()));
                    }
                }
            }
        }
        // For each class, reason the individuals and store them
        for (OWLClass c : onto.classesInSignature().toArray(OWLClass[]::new)){
            NodeSet<OWLNamedIndividual> individualsSet = reasoner.getInstances(c,false);
            OWLNamedIndividual[] individualsArray = individualsSet.entities().toArray(OWLNamedIndividual[]::new);
            for (OWLNamedIndividual individual: individualsArray) {
                G.add(String.format("%s,%s", c.getIRI().getFragment(), individual.getIRI().getFragment()));
            }
        }

        return G;
    }

    // Calculate the Effective Entailments
    private static HashMap<String, Float[]> calEffectiveness(ArrayList<ArrayList<String>> Gs, ArrayList<String> ents) {
        // Target entailment
        String g_t = "HeartDiseaseDiagnosis";
        // Create hash map to store entailments that co-exist and in-exist
        HashMap<String, Integer> co_ex = new HashMap<>();
        HashMap<String, Integer> co_inex = new HashMap<>();

        for (String g : ents) {
            co_ex.put(g, 0);
            co_inex.put(g, 0);
        }

        // For each entailment in each entailment closure, add one if both entailments
        // co-exist (in-exist) in both the learning domain and the target domain
        for (ArrayList<String> G : Gs) {
            for (String g : co_ex.keySet()) {
                if (G.contains(g) && G.contains(g_t)) {
                    co_ex.put(g, co_ex.get(g) + 1);
                }
                if (!G.contains(g) && !G.contains(g_t)) {
                    co_inex.put(g, co_inex.get(g) + 1);
                }
            }
        }

        // For each effective entailment we calculate its rate w.r.t the cardinality of
        // the set of entailment closures
        int n = Gs.size();
        HashMap<String, Float[]> eff = new HashMap<>();
        for (String g : co_ex.keySet()) {
            float e = co_ex.get(g) / (float) n;
            float ie = co_inex.get(g) / (float) n;
            Float[] f = {e, ie, e + ie};
            eff.put(g, f);
        }
        return eff;
    }

    // Calculate the Importance Entailments
    private static HashMap<String, Float> calImportance(ArrayList<ArrayList<String>> Gs) {
        // Create hash map to store the importance of the entailments
        HashMap<String, Float> imp = new HashMap<>();
        // For each entailment in each entailment closure, first set them to one and add one each
        // time the entailment appears
        for (ArrayList<String> G : Gs) {
            for (String g : G) {
                if (!imp.containsKey(g)) {
                    imp.put(g, (float) 1.0);
                } else {
                    imp.put(g, imp.get(g) + (float) 1.0);
                }
            }
        }
        // Calculate the rate of importance of each entailment w.r.t the cardinality
        // of the set of entailment closures
        for (String g : imp.keySet()) {
            imp.put(g, imp.get(g) / (float) Gs.size());
        }
        return imp;
    }

    // Method that takes an output file and write in them the given
    // ArrayList of entailments
    private static void output_ents(File f, ArrayList<String> ents) throws IOException {
        FileWriter writer = new FileWriter(f.getPath());
        for (String g : ents) {
            writer.write(String.format("%s\n", g));
        }
        writer.close();
    }

    // Method that get the names of the files in the ontology directory
    private static ArrayList<String> getFilesNames(String domain) {
        File directoryPath = new File(ONTO_DIR);
        ArrayList<String> filesList = new ArrayList<>();
        for (File f : directoryPath.listFiles()) {
            String name = f.getName();
            if (name.endsWith(".owl") && f.getName().contains(domain)) {
                filesList.add(name.split(".owl")[0]);
            }
        }
        return filesList;
    }

    // Method that get the paths of the files in the ontology directory
    private static ArrayList<String> getFilePaths(String domain) {

        File d_file = new File(ONTO_DIR);
        ArrayList<String> paths = new ArrayList<>();
        for (File f : d_file.listFiles()) {
            if (f.getAbsolutePath().endsWith(".owl") && f.getName().contains(domain)) {
                System.out.println("OWL File added:" + f);
                paths.add(f.getAbsolutePath());
            }
        }
        return paths;
    }

    // Method that calculates and store set of the entailment closure for the several ontologies
    public static ArrayList<ArrayList<String>> getEntClosures(String domain, String out_dir) throws OWLOntologyCreationException, IOException {

        ArrayList<ArrayList<String>> Gs = new ArrayList<>();
        // Create file to write output
        File ent_num_f = new File(out_dir + '/' + output_name + ".csv");
        // Creater writer
        FileWriter writer = new FileWriter(ent_num_f.getPath());
        // Create File object for the directory
        ArrayList<String> ontologiesForReasoning = getFilePaths(domain);
        ArrayList<String> ontologiesFileNames = getFilesNames(domain);

        System.out.println("Reasoning files "+ ontologiesFileNames);
        // For each ontology file calculate the entailment closure and add them
        for (int i = 0; i < getFilePaths(domain).size(); i++){
            loadOntology(ontologiesForReasoning.get(i));
            ArrayList<String> G = getEntClosure(localOnto);
            Gs.add(G);
            writer.write(String.format("%s,%d\n", ontologiesFileNames.get(i), G.size()));
        }
        writer.close();

        return Gs;
    }

}
