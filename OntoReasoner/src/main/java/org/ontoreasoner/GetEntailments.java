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
    private static String ONTO_DIR = "/home/juandiri/Desktop/ExplicabilityOntologyBasedML/RDFInsertions";
    // IRI of the ontology
    private static String ontoIRI = "http://www.cs.ox.ac.uk/isg/krr/ontologies/FlightOntology-1#";
    // Output name according to the query performed
    public static final String output_name = "DL_ATL_DFW";
    private static String ENT = "Entailments";
    public static OWLOntology localOnto;
    static OWLReasoner reasoner;
    static OWLReasonerFactory reasonerFactory;
    static OWLOntologyManager ontologyManager;
    static DefaultPrefixManager pm;

    public static void main(String args[]) throws OWLOntologyCreationException, IOException {
        if (args != null && args.length > 1) {
            ONTO_DIR = args[0];
        }

        File e_f = new File(ONTO_DIR, ENT);
        if (!e_f.exists()) {
            e_f.mkdir();
        }

        System.out.println("Files to read " + getFilePaths());
        System.out.println("Names of files " + getFilesNames());
        ArrayList<ArrayList<String>> Gs = getEntClosures(e_f.getPath());

        ArrayList<String> class_ents = new ArrayList<>();
        ArrayList<String> role_ents = new ArrayList<>();

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


        File class_ent_f = new File(e_f.getPath(), String.format("%s_class_ents.csv", output_name));
        File role_ent_f = new File(e_f.getPath(), String.format("%s_role_ents.csv", output_name));

        output_ents(class_ent_f, class_ents);
        output_ents(role_ent_f, role_ents);

        System.out.println("Calculate entailment importance \n");
        HashMap<String, Float> imp = calImportance(Gs);

        System.out.println("Calculate entailment effectiveness \n");
        ArrayList<String> ents = new ArrayList<>();
        ents.addAll(class_ents);
        ents.addAll(role_ents);
        HashMap<String, Float[]> eff = calEffectiveness(Gs, ents);


        File imp_f = new File(e_f.getPath(), String.format("%s_imp.csv", output_name));
        FileWriter imp_writer = new FileWriter(imp_f.getPath());
        for (String g : imp.keySet()) {
            imp_writer.write(String.format("%s:%f\n", g, imp.get(g)));
        }
        imp_writer.close();

        File eff_f = new File(e_f.getPath(), String.format("%s_eff.csv", output_name));
        FileWriter eff_writer = new FileWriter(eff_f.getPath());
        for (String g : eff.keySet()) {
            Float[] e = eff.get(g);
            eff_writer.write(String.format("%s:%f,%f,%f\n", g, e[0], e[1], e[2]));
        }
    }

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
        pm = new DefaultPrefixManager(null,null,"http://www.cs.ox.ac.uk/isg/krr/ontologies/FlightOntology-1#");
    }

//    public static ArrayList<OWLNamedIndividual> getDeparturesInstances(){
//        ArrayList<OWLNamedIndividual> departuresInstances = null;
//        // Get all the airports
//        OWLDataFactory fac = ontologyManager.getOWLDataFactory();
//        // Create IRI for the class "Departure"
//        OWLClass airports = fac.getOWLClass(IRI.create(pm.getDefaultPrefix(), "Departure"));
//        // Get Individuals for this class
//        NodeSet<OWLNamedIndividual> departureNodeSet = reasoner.getInstances(airports, false);
//        // Transform NodeSet into a Set
//        Set<OWLNamedIndividual> departureSet = departureNodeSet.getFlattened();
//        // Print individuals
//        for (OWLNamedIndividual departure : departureSet) {
//            System.out.println("Departure:" + pm.getShortForm(departure));
//            departuresInstances.add(departure);
//        }
//        return departuresInstances;
//    }

    public static ArrayList<String> getEntClosure(OWLOntology onto) {

        // Configure console process monitor
        ConsoleProgressMonitor progressMonitor = new ConsoleProgressMonitor();
        // Load default configuration for the reasoner
        OWLReasonerConfiguration config = new SimpleConfiguration(progressMonitor);

        // Create Reasoner Instance, classify the ontology and compute inferences
        reasoner = reasonerFactory.createReasoner(onto, config);

        ArrayList<String> G = new ArrayList<>();

        //Get all the individuals which are referenced in the ontology
        OWLNamedIndividual[] S = onto.individualsInSignature().toArray(OWLNamedIndividual[]::new);
        //Get all the object properties which are referenced in the ontology
        OWLObjectProperty[] OP = onto.objectPropertiesInSignature().toArray(OWLObjectProperty[]::new);

        // Calculate the entailments for each individual in the ontology
        for (OWLNamedIndividual individual:S) {
            for (OWLObjectProperty objectProperty: OP) {
                if (objectProperty.getIRI().equals("topObjectProperty")){
                    continue;
                }
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
        String g_t = "DepDelayed,dep";
        HashMap<String, Integer> co_ex = new HashMap<>();
        HashMap<String, Integer> co_inex = new HashMap<>();

        for (String g : ents) {
            co_ex.put(g, 0);
            co_inex.put(g, 0);
        }

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
        HashMap<String, Float> imp = new HashMap<>();
        for (ArrayList<String> G : Gs) {
            for (String g : G) {
                if (!imp.containsKey(g)) {
                    imp.put(g, (float) 1.0);
                } else {
                    imp.put(g, imp.get(g) + (float) 1.0);
                }
            }
        }
        for (String g : imp.keySet()) {
            imp.put(g, imp.get(g) / (float) Gs.size());
        }
        return imp;
    }

    // File Writer to store the entailments
    private static void output_ents(File f, ArrayList<String> ents) throws IOException {
        FileWriter writer = new FileWriter(f.getPath());
        for (String g : ents) {
            writer.write(String.format("%s\n", g));
        }
        writer.close();
    }

    // Method that get the names of the files in the ontology directory
    private static ArrayList<String> getFilesNames() {
        File directoryPath = new File(ONTO_DIR);
        ArrayList<String> filesList = new ArrayList<>();
        for (File f : directoryPath.listFiles()) {
            String name = f.getName();
            if (name.endsWith(".owl")) {
                filesList.add(name.split(".owl")[0]);
            }
        }
        return filesList;
    }

    // Method that get the paths of the files in the ontology directory
    private static ArrayList<String> getFilePaths() {

        File d_file = new File(ONTO_DIR);
        ArrayList<String> paths = new ArrayList<>();
        for (File f : d_file.listFiles()) {
            if (f.getAbsolutePath().endsWith(".owl")) {
                System.out.println("OWL File added:" + f);
                paths.add(f.getAbsolutePath());
            }
        }
        return paths;
    }

    // Method that calculates and store the entailment closure for several ontologies
    public static ArrayList<ArrayList<String>> getEntClosures(String out_dir) throws OWLOntologyCreationException, IOException {

        ArrayList<ArrayList<String>> Gs = new ArrayList<>();
        // Create file to write output
        File ent_num_f = new File(out_dir + '/' + output_name + ".csv");
        // Creater writer
        FileWriter writer = new FileWriter(ent_num_f.getPath());
        // Create File object for the directory
        ArrayList<String> ontologiesForReasoning = getFilePaths();
        ArrayList<String> ontologiesFileNames = getFilesNames();
        System.out.println("Reasoning files "+ ontologiesFileNames);
        for (int i = 0; i < getFilePaths().size(); i++){
            loadOntology(ontologiesForReasoning.get(i));
            ArrayList<String> G = getEntClosure(localOnto);
            Gs.add(G);
            writer.write(String.format("%s,%d\n", ontologiesFileNames.get(i), G.size()));
            writer.close();

        }

        return Gs;
    }

}
