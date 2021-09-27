import unittest
import os
import sys
from random import sample
from rdflib import RDF,BNode

sys.path.insert(0, os.path.join(".."))
sys.path.insert(0, os.path.join("..",".."))

from builder.instance import InstanceBuilder

curr_dir = os.path.dirname(os.path.realpath(__file__))
instance_file = os.path.join(curr_dir,"..","files","nor_gate.xml")
model_file = os.path.join(curr_dir,"..","..","utility","nv_model.xml")

def _graph_element_check(graph):
    node_id_map = {}
    for n,v,e in graph.edges(keys=True):
        n_data = graph.nodes[n]
        v_data = graph.nodes[v]
        if n in node_id_map.keys():
            if node_id_map[n] != n_data["key"]:
                return False
        else:
            node_id_map[n] = n_data["key"]
        if v in node_id_map.keys():
            if node_id_map[v] != v_data["key"]:
                return False
        else:
            node_id_map[v] = v_data["key"]
    return True

class TestSearch(unittest.TestCase):
    def setUp(self):
        self.builder = InstanceBuilder(model_file,instance_file)
        self.graph = self.builder._graph

    def tearDown(self):
        pass
    
    def test_get_methods(self):
        expected_entities = [(k,v,e) for k,v,e in self.graph.search((None,RDF.type,None)) if not isinstance(k[1]["key"],BNode)]
        actual_entities = self.builder.get_entity() 
        a_diff = diff(expected_entities,actual_entities)
        self.assertEqual(len(a_diff),0)
        for k,v,e in self.builder.get_interaction():
            k,k_data = k
            v,v_data = v
            actual_consists = self.builder.get_consistsof(k)            
            expected_consists = self.graph.search((k,self.builder._model_graph.identifiers.predicates.consistsOf,None))
            c_diff = diff(expected_consists,actual_consists)
            self.assertEqual(len(c_diff),0)

    def test_get_entities(self):
        rdf_types = [c[0][1]["key"] for c in self.graph.search((None,RDF.type,None))]
        for res,data in self.builder.get_entities():
            self.assertIn(data["key"],rdf_types)
    
    def test_get_children(self):
        for entity,data in self.builder.get_entities():
            a_children = self.builder.get_children(entity)
            e_children = [c[1] for c in self.graph.search((entity,None,None))]
            for child,predicate in a_children:
                self.assertIn(child,e_children)
    
    def test_get_parents(self):
        for entity,data in self.builder.get_entities():
            a_parents = self.builder.get_parents(entity)
            e_parents = [c[0] for c in self.graph.search((None,None,entity))]
            for parent,predicate in a_parents:
                self.assertIn(parent,e_parents)

    def test_get_entity_depth(self):
        for entity,data in self.builder.get_entities():
            depth = self.builder.get_entity_depth(entity)
            if self.builder.get_parents(entity) == []:
                self.assertEqual(depth,0)
            else:
                self.assertGreater(depth, 0)


class TestViews(unittest.TestCase):
    def setUp(self):
        self.builder = InstanceBuilder(model_file,instance_file)
        self.model = self.builder._model_graph

    def tearDown(self):
        pass

    def test_pruned(self):
        self.builder.set_pruned_view()
        graph = self.builder.view
        for n,v,e in graph.edges(keys=True):
            self.assertIn(e,self.model.identifiers.predicates)

    def test_heirarchy(self):
        self.builder.set_hierarchy_view()
        graph = self.builder.view
        for n,data in graph.nodes(data=True):
            actual_children = [[c[1],graph.nodes[c[1]]] for c in graph.edges(n)]
            expected_children = [c[0] for c in self.builder.get_children(n)]
            self.assertEqual(expected_children, actual_children)

    def test_interaction_explicit(self):
        self.builder.set_interaction_explicit_view()
        graph = self.builder.view
        self.assertTrue(_graph_element_check(graph))
        interaction_obj = self.model.identifiers.objects.interaction
        physical_entity_obj = self.model.identifiers.objects.physical_entity
        direction_pred = self.model.identifiers.predicates.direction
        input_pred = self.model.identifiers.objects.input
        output_pred = self.model.identifiers.objects.output
        interaction_class_code = self.model.get_class_code(interaction_obj)
        pe_class_code = self.model.get_class_code(physical_entity_obj)
        interactions_classes = [d[1]["key"] for d in self.model.get_derived(interaction_class_code)]
        interaction_predicates = {k[1]["key"]:v[1]["key"] for (k,v,e) in self.model.search((None,direction_pred,None))}
        for n,v,e in graph.edges(keys=True):
            if self.builder.get_rdf_type(n)[1]["key"] in interactions_classes:
                self.assertEqual(interaction_predicates[e],output_pred)
                e_type = self.builder.get_rdf_type(v)[1]["key"]
                self.assertTrue(self.model.is_derived(e_type,pe_class_code))
            elif self.builder.get_rdf_type(v)[1]["key"] in interactions_classes:
                self.assertEqual(interaction_predicates[e],input_pred)
                e_type = self.builder.get_rdf_type(n)[1]["key"]
                self.assertTrue(self.model.is_derived(e_type,pe_class_code))
            else:
                self.fail("Neither node is an interaction.")

    def test_interaction_verbose(self):
        self.builder.set_interaction_verbose_view()
        graph = self.builder.view
        self.assertTrue(_graph_element_check(graph))
        interaction_obj = self.model.identifiers.objects.interaction
        physical_entity_obj = self.model.identifiers.objects.physical_entity
        direction_pred = self.model.identifiers.predicates.direction
        input_pred = self.model.identifiers.objects.input
        output_pred = self.model.identifiers.objects.output
        interaction_class_code = self.model.get_class_code(interaction_obj)
        pe_class_code = self.model.get_class_code(physical_entity_obj)
        interactions_classes = [d[1]["key"] for d in self.model.get_derived(interaction_class_code)]
        interaction_predicates = {k[1]["key"]:v[1]["key"] for (k,v,e) in self.model.search((None,direction_pred,None))}
        for n,v,e in graph.edges(keys=True):
            if self.builder.get_rdf_type(n)[1]["key"] in interactions_classes:
                self.assertEqual(interaction_predicates[e],output_pred)
                e_type = self.builder.get_rdf_type(v)[1]["key"]
                self.assertTrue(self.model.is_derived(e_type,pe_class_code))
            elif self.builder.get_rdf_type(v)[1]["key"] in interactions_classes:
                self.assertEqual(interaction_predicates[e],input_pred)
                e_type = self.builder.get_rdf_type(n)[1]["key"]
                self.assertTrue(self.model.is_derived(e_type,pe_class_code))
            else:
                self.fail("Neither node is an interaction.")
    
    def test_interaction(self):
        self.builder.set_interaction_view()
        graph = self.builder.view
        self.assertTrue(_graph_element_check(graph))
        interaction_obj = self.model.identifiers.objects.interaction
        physical_entity_obj = self.model.identifiers.objects.physical_entity
        interaction_class_code = self.model.get_class_code(interaction_obj)
        pe_class_code = self.model.get_class_code(physical_entity_obj)
        interactions_classes = [d[1]["key"] for d in self.model.get_derived(interaction_class_code)]
        pe_classes = [d[1]["key"] for d in self.model.get_derived(pe_class_code)]
        for n,v,e in graph.edges(keys=True):
            self.assertIn(e,interactions_classes)
            self.assertIn(self.builder.get_rdf_type(n)[1]["key"],pe_classes)
            self.assertIn(self.builder.get_rdf_type(v)[1]["key"],pe_classes)
            

    def test_interaction_genetic(self):
        self.builder.set_interaction_genetic_view()
        graph = self.builder.view
        self.assertTrue(_graph_element_check(graph))
        interaction_obj = self.model.identifiers.objects.interaction
        physical_entity_obj = self.model.identifiers.objects.physical_entity
        interaction_class_code = self.model.get_class_code(interaction_obj)
        pe_class_code = self.model.get_class_code(physical_entity_obj)
        interactions_classes = [d[1]["key"] for d in self.model.get_derived(interaction_class_code)]
        pe_classes = [d[1]["key"] for d in self.model.get_derived(pe_class_code)]
        for n,v,e in graph.edges(keys=True):
            self.assertIn(e,interactions_classes)
            self.assertIn(self.builder.get_rdf_type(n)[1]["key"],pe_classes)
            self.assertIn(self.builder.get_rdf_type(v)[1]["key"],pe_classes)

    def test_interaction_protein(self):
        self.fail("Not Implemented.")

class TestModes(unittest.TestCase):
        def setUp(self):
            self.builder = InstanceBuilder(model_file,instance_file)

        def tearDown(self):
            pass
        
        def test_sub_tree(self):
            rand_sample_num = 20
            sub_edges = sample(list(self.builder.edges(keys=True,data=True)),rand_sample_num)
            node_attrs = {}
            for n,v,k,e in sub_edges:
                node_attrs[n] = self.builder.nodes[n]
                node_attrs[v] = self.builder.nodes[v]
                
            sub_graph = self.builder.sub_graph(sub_edges,node_attrs)
            self.assertIsInstance(sub_graph,self.builder._graph.__class__)
            self.assertEqual(len(sub_graph.edges),rand_sample_num)
            graph_triples = [e for n,v,e in self.builder.edges]
            sub_triples = [e for n,v,e in sub_graph.edges]
            [self.assertIn(sub_triple,graph_triples) for sub_triple in sub_triples]
            self.assertCountEqual(sub_edges,sub_graph.edges(keys=True,data=True))
            self.assertTrue(_graph_element_check(sub_graph))

            for n,v,k,e in sub_graph.edges(data=True,keys=True):
                n_data = sub_graph.nodes[n]
                n_data_orig = self.builder.nodes[n]
                self.assertTrue(n_data == n_data_orig)
                v_data = sub_graph.nodes[v]
                v_data_orig = self.builder.nodes[v]
                self.assertTrue(v_data == v_data_orig)
                orig_edge_data = self.builder.edges[n,v,k]
                self.assertEqual(orig_edge_data,e)

        def test_get_tree(self):
            self.builder.set_tree_mode()
            tree_graph = self.builder.view
            self.assertIsInstance(tree_graph,self.builder._graph.__class__)
            self.assertTrue(_graph_element_check(tree_graph))
            self.assertEqual(len(self.builder.edges),len(tree_graph.edges))
            self.assertNotEqual(len(self.builder.nodes),len(tree_graph.nodes))
            for n,v,e in tree_graph.edges:
                n_data = tree_graph.nodes[n]
                v_data = tree_graph.nodes[v]
                try:
                    orig_n_data = self.builder.nodes[n]
                    self.assertEqual(n_data,orig_n_data)
                except KeyError:
                    orig_node_id = [x for x,y in self.builder.nodes(data=True) if y['key'] == n_data["key"]]
                    self.assertEqual(len(orig_node_id),1)
                    orig_node_id = orig_node_id[0]
                    self.assertEqual(tree_graph.nodes[orig_node_id],n_data)
                try:
                    orig_v_data = self.builder.nodes[v]
                    self.assertEqual(v_data,orig_v_data)
                except KeyError:
                    orig_node_id = [x for x,y in self.builder.nodes(data=True) if y['key'] == v_data["key"]]
                    self.assertEqual(len(orig_node_id),1)
                    orig_node_id = orig_node_id[0]
                    self.assertEqual(tree_graph.nodes[orig_node_id],v_data)
            g_search = self.builder._graph.search((None,RDF.type,None))
            for n,v,e in g_search:
                n_id,n_data = n
                v_id,v_data = v
                t_n_data = tree_graph.nodes[n_id]
                t_v_data = tree_graph.nodes[v_id]
                self.assertEqual(n_data,t_n_data)
                self.assertEqual(v_data,t_v_data)

                t_search = tree_graph.search((n_id,None,None))
                for n1,v1,e1 in t_search:
                    self.assertEqual(n1,n)





def diff(list1,list2):
    diff = []
    for n,v,e in list1:
        for n1,v1,e1 in list2:
            if n == n1 and v == v1 and e == e1:
                break
        else:
            diff.append((n,v,e,k))
    return diff


if __name__ == '__main__':
    unittest.main()
