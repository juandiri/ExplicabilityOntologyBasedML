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
import java.util.HashMap;

public class GetEntailments {

    // Directory where the ontologies are contained
    private static String HOME_DIR = "your home dir";
    // IRI of the ontology
    private static String ontoIRI = "http://www.cs.ox.ac.uk/isg/krr/ontologies/FlightOntology-1#";
    private static String ENT = "Entailments";
    public static OWLOntology localOnto;

    // Create the IRI
    IRI location = IRI.create(ontoIRI);

    public static void main(String args[]) throws OWLOntologyCreationException, IOException {
        if (args != null && args.length > 1) {
            HOME_DIR = args[0];
        }

        File e_f = new File(HOME_DIR, ENT);
        if (!e_f.exists()) {
            e_f.mkdir();
        }
        ArrayList<String> doms = getFilePaths();
        for (String dom : doms) {
            System.out.printf("\n Domain: %s \n\n", dom);

            ArrayList<ArrayList<String>> Gs = getEntClosures(dom, e_f);

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
            File class_ent_f = new File(e_f.getPath(), String.format("%s_class_ents.csv", dom));
            File role_ent_f = new File(e_f.getPath(), String.format("%s_role_ents.csv", dom));

            (class_ent_f, class_ents);
            output_ents(role_ent_f, role_ents);


            System.out.println("Calculate entailment importance \n");
            HashMap<String, Float> imp = calImportance(Gs);

            System.out.println("Calculate entailment effectiveness \n");
            ArrayList<String> ents = new ArrayList<>();
            ents.addAll(class_ents);
            ents.addAll(role_ents);
            HashMap<String, Float[]> eff = calEffectiveness(Gs, ents);


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

    public OWLOntology loadOntology(String ontology_filepath) throws OWLOntologyCreationException{

        IRI location = IRI.create("http://www.cs.ox.ac.uk/isg/krr/ontologies/FlightOntology-1#");
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
                        G.add(String.format("%s,%s,%s", individual.toStringID().substring(ontoIRI.length()),
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

    private static void output_ents(File f, ArrayList<String> ents) throws IOException {
        FileWriter writer = new FileWriter(f.getPath());
        for (String g : ents) {
            writer.write(String.format("%s\n", g));
        }
        writer.close();
    }

    private static ArrayList<String> getFilesNames() {
        File directoryPath = new File(HOME_DIR);
        ArrayList<String> filesList = new ArrayList<>();
        for (File f : directoryPath.listFiles()) {
            String name = f.getName();
            if (name.endsWith(".owl")) {
                filesList.add(name.split(".owl")[0]);
            }
        }
        return filesList;
    }

    private static ArrayList<String> getFilePaths() {

        File d_file = new File(HOME_DIR);
        ArrayList<String> paths = new ArrayList<>();
        for (File f : d_file.listFiles()) {
            if (! f.getAbsolutePath().endsWith(".owl")) {
                paths.add(f.getAbsolutePath());
            }
        }
        return paths;
    }

    public ArrayList<ArrayList<String>> getEntClosures(String out_dir, String e_f) throws OWLOntologyCreationException, IOException {

        ArrayList<ArrayList<String>> Gs = new ArrayList<>();
        // Create file to write output
        File ent_num_f = new File(e_f, String.format("%s/ent_num.csv", out_dir));
        // Create File object for the directory
        ArrayList<String> filesInDirectory = getFilePaths();
        // List of all files and directories
        ArrayList<String> fileNames = getFilesNames();
        for (String f : filesInDirectory){
            OWLOntology ontologyFile = loadOntology(f);
            ArrayList<String> G = getEntClosure();
            Gs.add(G);
            writer.write(String.format("%s,%d\n", snp_ids.get(i), G.size()));
            if (i % 100 == 0) {
                System.out.printf("%d: %s, %d \n", i, snp_ids.get(i), G.size());
            }
            writer.close();


        }
        return Gs;
    }

}
