import unittest
import os
import sys
import re

from rdflib import BNode

sys.path.insert(0, os.path.join(".."))

from visual.handlers.abstract_color import color_list
from visual.instance import InstanceVisual
from visual.model import ModelVisual
curr_dir = os.path.dirname(os.path.realpath(__file__))
model_fn = os.path.join(curr_dir,"..","utility","nv_model.xml")

class TestModel(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    class TestPresets(unittest.TestCase):
        def setUp(self):
            self.visual = ModelVisual(model_fn)

        def tearDown(self):
            pass
        
        def test_heirarchy(self):
            self.fail("Untested.")
        
        def test_requirements(self):
            self.fail("Untested.")
    
    class TestLabels(unittest.TestCase):
        def setUp(self):
            self.visual = ModelVisual(model_fn)

        def tearDown(self):
            pass

    class TestColor(unittest.TestCase):        
        class TestNode(unittest.TestCase):
            def setUp(self):
                self.visual = ModelVisual(model_fn)

            def tearDown(self):
                pass

            def test_standard(self):
                view = self.visual._builder.view
                colors = self.visual.add_standard_node_color()
                self.assertEqual(len(colors), len(view.nodes))
                for index,(node,data) in enumerate(view.nodes(data=True)):
                    self.assertEqual(colors[index], {"standard" : color_list[0]})

                self.visual.set_heirarchy_view()
                self.visual.set_heirarchy_view()

                view = self.visual._builder.view
                colors = self.visual.add_standard_node_color()
                self.assertEqual(len(colors), len(view.nodes))
                for index,(node,data) in enumerate(view.nodes(data=True)):
                    self.assertEqual(colors[index], {"standard" : color_list[0]})

            def test_rdf_type(self):
                view = self.visual._builder.view
                ret_val = self.visual.add_rdf_type_node_color()
                self.assertIsNone(ret_val)

                colors = self.visual.add_rdf_type_node_color()
                self.assertEqual(len(colors), len(view.nodes))
                for index,(node,data) in enumerate(view.nodes(data=True)):
                    if self.visual._builder.get_rdf_type(node) is None:
                        self.assertEqual(colors[index], {"no_type" : color_list[1]} )
                    else:
                        self.assertEqual(colors[index], {"rdf_type" :  color_list[0]} )
                self.visual.set_heirarchy_view()
                self.visual.set_heirarchy_view()

                view = self.visual._builder.view
                colors = self.visual.add_rdf_type_node_color()
                self.assertEqual(len(colors), len(view.nodes))
                for index,(node,data) in enumerate(view.nodes(data=True)):
                    if self.visual._builder.get_rdf_type(node) is None:
                        self.assertEqual(colors[index], {"no_type" :  color_list[1]} )
                    else:
                        self.assertEqual(colors[index], {"rdf_type" :  color_list[0]} )

            def test_class(self):
                view = self.visual._builder.view
                ret_val = self.visual.add_class_node_color()
                self.assertIsNone(ret_val)
                colors = self.visual.add_class_node_color()

                print(colors)

            def test_branch(self):
                self.fail("Untested.")

            def test_heirarchy(self):
                self.fail("Untested.")
            

        class TestEdge(unittest.TestCase):
            def setUp(self):
                self.visual = ModelVisual(model_fn)

            def tearDown(self):
                pass
            
            def test_standard(self):
                pass

            def test_type(self):
                self.fail("Untested.")

    class TestShape(unittest.TestCase):
        def setUp(self):
            self.visual = ModelVisual(model_fn)

        def tearDown(self):
            pass
        
    class TestSize(unittest.TestCase):
        def setUp(self):
            self.visual = ModelVisual(model_fn)
            self.builder = self.visual._builder
            self.standard_node_size = self.visual._size_h._standard_node_size

        def tearDown(self):
            pass

        def test_heirarchy(self):
            ret = self.visual.add_heirachy_node_size()
            self.assertIsNone(ret)

            node_sizes = self.visual.add_heirachy_node_size()
            self.assertEqual(len(node_sizes),len(self.builder.v_nodes()))
            for index,(node,data) in enumerate(self.builder.v_nodes(data=True)):
                node_size = node_sizes[index]
                key = data["key"]
                if isinstance(key,BNode):
                    self.assertEqual(node_size,self.standard_node_size)
                elif self.builder.get_rdf_type(node) == []:
                    self.assertEqual(node_size,self.standard_node_size)
                else:
                    depth = self.builder.get_class_depth(node)
                    if depth == 0:
                        self.assertEqual(node_size,self.standard_node_size)
                    else:
                        self.assertEqual(node_size,self.standard_node_size/depth)


class TestInstance(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    class TestPresets(unittest.TestCase):
        def setUp(self):
            filename = os.path.join(curr_dir,"files","nor_gate.xml")
            self.visualiser = NVisualiser(filename)

        def tearDown(self):
            None

        def test_heirarchy(self):
            self.visualiser.set_heirarchy_preset()
            self.visualiser.build()

    class TestLabels(unittest.TestCase):

        def setUp(self):
            filename = os.path.join(curr_dir,"files","0x3B.xml")
            self.visualiser = NVisualiser(filename)

        def tearDown(self):
            None

        def test_node_none(self):
            view = self.visualiser._builder.view
            labels = self.visualiser.add_node_no_labels()
            self.assertEqual(len(labels), len(view.nodes))
            for index,(node,data) in enumerate(view.nodes(data=True)):
                self.assertIsNone(labels[index])

            self.visualiser.set_heirarchy_view()
            self.visualiser.set_heirarchy_view()

            view = self.visualiser._builder.view
            labels = self.visualiser.add_node_no_labels()
            self.assertEqual(len(labels), len(view.nodes))
            for index,(node,data) in enumerate(view.nodes(data=True)):
                self.assertIsNone(labels[index])

        def test_node_adjacency(self):
            view = self.visualiser._builder.view
            ret_val = self.visualiser.add_node_adjacency_labels()
            self.assertIsNone(ret_val)

            labels = self.visualiser.add_node_adjacency_labels()
            self.assertEqual(len(labels), len(view.nodes))
            for index,(node,data) in enumerate(view.nodes(data=True)):
                split = labels[index].split(",")
                actual_in = int(split[0].split(":")[1])
                actual_out = int(split[1].split(":")[1])
                expected_in = view._graph.in_edges(node)
                expected_out = view._graph.out_edges(node)
                self.assertEqual(actual_in, len(expected_in))
                self.assertEqual(actual_out, len(expected_out))

            self.visualiser.set_heirarchy_view()
            self.visualiser.set_heirarchy_view()
            
            view = self.visualiser._builder.view
            labels = self.visualiser.add_node_adjacency_labels()
            self.assertEqual(len(labels), len(view.nodes))
            for index,(node,data) in enumerate(view.nodes(data=True)):
                split = labels[index].split(",")
                actual_in = int(split[0].split(":")[1])
                actual_out = int(split[1].split(":")[1])
                expected_in = view._graph.in_edges(node)
                expected_out = view._graph.out_edges(node)
                self.assertEqual(actual_in, len(expected_in))
                self.assertEqual(actual_out, len(expected_out))
                
        def test_node_name(self):
            view = self.visualiser._builder.view
            ret_val = self.visualiser.add_node_name_labels()
            self.assertIsNone(ret_val)

            labels = self.visualiser.add_node_name_labels()
            self.assertEqual(len(labels), len(view.nodes))
            for index,(node,data) in enumerate(view.nodes(data=True)):
                self.assertEqual(_get_name(data["key"]), labels[index])

            self.visualiser.set_heirarchy_view()
            self.visualiser.set_heirarchy_view()
            
            view = self.visualiser._builder.view
            labels = self.visualiser.add_node_name_labels()
            self.assertEqual(len(labels), len(view.nodes))
            for index,(node,data) in enumerate(view.nodes(data=True)):
                self.assertEqual(_get_name(data["key"]), labels[index])

        def test_node_class_type(self):
            view = self.visualiser._builder.view
            ret_val = self.visualiser.add_node_type_labels()
            self.assertIsNone(ret_val)

            labels = self.visualiser.add_node_type_labels()
            self.assertEqual(len(labels), len(view.nodes))
            for index,(node,data) in enumerate(view.nodes(data=True)):
                n_type = self.visualiser._builder.get_rdf_type(node)
                if n_type is not None:
                    actual_type = labels[index]
                    expected_type = _get_name(n_type[1]["key"])
                    self.assertEqual(expected_type,actual_type)
                elif data["type"] == "URI":
                    self.assertEqual(labels[index], "Identifier")
                elif data["type"] == "URI":
                    self.assertEqual(labels[index], "Literal")
                else:
                    self.assertEqual(labels[index], "?")

            self.visualiser.set_heirarchy_view()
            self.visualiser.set_heirarchy_view()
            
            view = self.visualiser._builder.view
            labels = self.visualiser.add_node_type_labels()
            self.assertEqual(len(labels), len(view.nodes))
            for index,(node,data) in enumerate(view.nodes(data=True)):
                n_type = self.visualiser._builder.get_rdf_type(node)
                if n_type is not None:
                    actual_type = labels[index]
                    expected_type = _get_name(n_type[1]["key"])
                    self.assertEqual(expected_type,actual_type)
                elif data["type"] == "URI":
                    self.assertEqual(labels[index], "Identifier")
                elif data["type"] == "URI":
                    self.assertEqual(labels[index], "Literal")
                else:
                    self.assertEqual(labels[index], "?")
        
        def test_node_role(self):
            pass

        def test_edge_none(self):
            view = self.visualiser._builder.view
            labels = self.visualiser.add_edge_no_labels()
            self.assertEqual(len(labels), len(view.edges))
            for index,(n,v,k,e) in enumerate(view.edges(keys=True,data=True)):
                self.assertIsNone(labels[index])

            self.visualiser.set_heirarchy_view()
            self.visualiser.set_heirarchy_view()

            view = self.visualiser._builder.view
            labels = self.visualiser.add_edge_no_labels()
            self.assertEqual(len(labels), len(view.edges))
            for index,(n,v,k,e) in enumerate(view.edges(keys=True,data=True)):
                self.assertIsNone(labels[index])

        def test_edge_name(self):
            view = self.visualiser._builder.view
            ret_val = self.visualiser.add_edge_name_labels()
            self.assertIsNone(ret_val)

            labels = self.visualiser.add_edge_name_labels()
            self.assertEqual(len(labels), len(view.edges))
            for index,(n,v,k,e) in enumerate(view.edges(keys=True,data=True)):
                self.assertEqual(_get_name(e["display_name"]), labels[index])

            self.visualiser.set_heirarchy_view()
            self.visualiser.set_heirarchy_view()

            view = self.visualiser._builder.view
            labels = self.visualiser.add_edge_name_labels()
            self.assertEqual(len(labels), len(view.edges))
            for index,(n,v,k,e) in enumerate(view.edges(keys=True,data=True)):
                self.assertEqual(_get_name(e["display_name"]), labels[index])

    class TestColor(unittest.TestCase):

        def setUp(self):
            filename = os.path.join(curr_dir,"files","0x3B.xml")
            self.visualiser = NVisualiser(filename)

        def tearDown(self):
            None

        def test_node_standard(self):
            view = self.visualiser._builder.view
            colors = self.visualiser.add_standard_node_color()
            self.assertEqual(len(colors), len(view.nodes))
            for index,(node,data) in enumerate(view.nodes(data=True)):
                self.assertEqual(colors[index], {"standard" : StandardPalette.primary.value} )

            self.visualiser.set_heirarchy_view()
            self.visualiser.set_heirarchy_view()

            view = self.visualiser._builder.view
            colors = self.visualiser.add_standard_node_color()
            self.assertEqual(len(colors), len(view.nodes))
            for index,(node,data) in enumerate(view.nodes(data=True)):
                self.assertEqual(colors[index], {"standard" : StandardPalette.primary.value} )

        def test_node_class(self):
            view = self.visualiser._builder.view
            ret_val = self.visualiser.add_rdf_type_node_color()
            self.assertIsNone(ret_val)

            colors = self.visualiser.add_rdf_type_node_color()
            self.assertEqual(len(colors), len(view.nodes))
            for index,(node,data) in enumerate(view.nodes(data=True)):
                if self.visualiser._builder.get_rdf_type(node) is None:
                    self.assertEqual(colors[index], {"no_type" : StandardPalette.secondary.value} )
                else:
                    self.assertEqual(colors[index], {"rdf_type" : StandardPalette.primary.value} )
            self.visualiser.set_heirarchy_view()
            self.visualiser.set_heirarchy_view()

            view = self.visualiser._builder.view
            colors = self.visualiser.add_rdf_type_node_color()
            self.assertEqual(len(colors), len(view.nodes))
            for index,(node,data) in enumerate(view.nodes(data=True)):
                if self.visualiser._builder.get_rdf_type(node) is None:
                    self.assertEqual(colors[index], {"no_type" : StandardPalette.secondary.value} )
                else:
                    self.assertEqual(colors[index], {"rdf_type" : StandardPalette.primary.value} )

        def test_node_role(self):
            pass
        def test_node_class_type(self):
            pass

        def test_edge_standard(self):
            view = self.visualiser._builder.view
            colors = self.visualiser.add_standard_edge_color()
            self.assertEqual(len(colors), len(view.edges))
            for index,(n,v,e) in enumerate(view.edges(data=True)):
                self.assertEqual(colors[index], {"standard" : "#888"} )

            self.visualiser.set_heirarchy_view()
            self.visualiser.set_heirarchy_view()

            view = self.visualiser._builder.view
            colors = self.visualiser.add_standard_edge_color()
            self.assertEqual(len(colors), len(view.edges))
            for index,(n,v,e) in enumerate(view.edges(data=True)):
                self.assertEqual(colors[index], {"standard" : "#888"})
        def test_edge_predicate(self):
            pass
        def test_node_interaction(self):
            pass

    class TestShape(unittest.TestCase):
        def setUp(self):
            filename = os.path.join(curr_dir,"files","0x3B.xml")
            self.visualiser = NVisualiser(filename)

        def tearDown(self):
            None
        
        def test_adaptive_node(self):
            view = self.visualiser._builder.view
            ret_val = self.visualiser.set_adaptive_node_shape()
            self.assertIsNone(ret_val)
            s_list = self.visualiser._shape_h.node.shapes
            default_shape = s_list[0]
            shapes_l = s_list[1:]
            counter = 0
            shape_map = {"no_type" : default_shape}


            shapes = self.visualiser.set_adaptive_node_shape()
            self.assertEqual(len(shapes), len(view.nodes))
            for index,(node,data) in enumerate(view.nodes(data=True)):
                n_type = self.visualiser._builder.get_rdf_type(node)
                if n_type is None:
                    expected_shape = {"No Type" : shape_map["no_type"]}
                else:
                    n_type = n_type[1]["key"]
                    if n_type not in shape_map.keys():
                        shape_map[n_type] = shapes_l[counter]
                        counter = counter + 1
                    expected_shape = {_get_name(n_type) : shape_map[n_type]}
                self.assertEqual(shapes[index], expected_shape)
                    

            self.visualiser.set_heirarchy_view()
            self.visualiser.set_heirarchy_view()

            shape_map = {"no_type" : default_shape}
            view = self.visualiser._builder.view
            shapes = self.visualiser.set_adaptive_node_shape()
            counter = 0
            self.assertEqual(len(shapes), len(view.nodes))

            for index,(node,data) in enumerate(view.nodes(data=True)):
                n_type = self.visualiser._builder.get_rdf_type(node)
                if n_type is None:
                    expected_shape = {"No Type" : shape_map["no_type"]}
                else:
                    n_type = n_type[1]["key"]
                    if n_type not in shape_map.keys():
                        shape_map[n_type] = shapes_l[counter]
                        counter = counter + 1
                    expected_shape = {_get_name(n_type) : shape_map[n_type]}
                self.assertEqual(shapes[index], expected_shape)

    class TestSize(unittest.TestCase):
        def setUp(self):
            filename = os.path.join(curr_dir,"files","0x3B.xml")
            self.visualiser = NVisualiser(filename)

        def tearDown(self):
            None

        def test_standard(self):
            view = self.visualiser._builder.view
            standard_node_size = self.visualiser._size_h._standard_node_size
            sizes = self.visualiser.add_standard_node_size()
            self.assertEqual(len(sizes), len(view.nodes))
            for index,(node,data) in enumerate(view.nodes(data=True)):
                self.assertEqual(sizes[index], standard_node_size)

            self.visualiser.set_heirarchy_view()
            self.visualiser.set_heirarchy_view()

            view = self.visualiser._builder.view
            sizes = self.visualiser.add_standard_node_size()
            self.assertEqual(len(sizes), len(view.nodes))
            for index,(node,data) in enumerate(view.nodes(data=True)):
                self.assertEqual(sizes[index], standard_node_size)

        def test_rdf_type(self):
            view = self.visualiser._builder.view
            ret_val = self.visualiser.add_rdf_type_node_size()
            self.assertIsNone(ret_val)

            standard_node_size = self.visualiser._size_h._standard_node_size
            sizes = self.visualiser.add_rdf_type_node_size()
            self.assertEqual(len(sizes), len(view.nodes))
            for index,(node,data) in enumerate(view.nodes(data=True)):
                if self.visualiser._builder.get_rdf_type(node):
                    self.assertEqual(sizes[index], standard_node_size)
                else:
                    self.assertEqual(sizes[index], standard_node_size/2)

            self.visualiser.set_heirarchy_view()
            self.visualiser.set_heirarchy_view()

            view = self.visualiser._builder.view
            sizes = self.visualiser.add_rdf_type_node_size()
            self.assertEqual(len(sizes), len(view.nodes))
            for index,(node,data) in enumerate(view.nodes(data=True)):
                if self.visualiser._builder.get_rdf_type(node):
                    self.assertEqual(sizes[index], standard_node_size)
                else:
                    self.assertEqual(sizes[index], standard_node_size/2)

        def test_centrality(self):
            view = self.visualiser._builder.view
            ret_val = self.visualiser.add_centrality_node_size()
            self.assertIsNone(ret_val)

            standard_node_size = self.visualiser._size_h._standard_node_size
            sizes = self.visualiser.add_centrality_node_size()
            self.assertEqual(len(sizes), len(view.nodes))
            for index,(node,data) in enumerate(view.nodes(data=True)):
                expected_size = 1 + len(view._graph.in_edges(node)) + len(view._graph.out_edges(node))
                expected_size = int((expected_size * standard_node_size) / 4)
                if expected_size > 100:
                    expected_size = 100
                if expected_size < standard_node_size/2:
                    expected_size = standard_node_size
                self.assertEqual(sizes[index], expected_size)
                    
            self.visualiser.set_heirarchy_view()
            self.visualiser.set_heirarchy_view()

            view = self.visualiser._builder.view
            sizes = self.visualiser.add_centrality_node_size()
            self.assertEqual(len(sizes), len(view.nodes))
            for index,(node,data) in enumerate(view.nodes(data=True)):
                expected_size = 1 + len(view._graph.in_edges(node)) + len(view._graph.out_edges(node))
                expected_size = int((expected_size * standard_node_size) / 4)
                if expected_size > 100:
                    expected_size = 100
                if expected_size < standard_node_size/2:
                    expected_size = standard_node_size
                self.assertEqual(sizes[index], expected_size)

        def test_in_centrality(self):
            view = self.visualiser._builder.view
            ret_val = self.visualiser.add_in_centrality_node_size()
            self.assertIsNone(ret_val)

            standard_node_size = self.visualiser._size_h._standard_node_size
            sizes = self.visualiser.add_in_centrality_node_size()
            self.assertEqual(len(sizes), len(view.nodes))
            for index,(node,data) in enumerate(view.nodes(data=True)):
                expected_size = 1 + len(view._graph.in_edges(node))
                expected_size = int((expected_size * standard_node_size) / 2)
                if expected_size > 100:
                    expected_size = 100
                if expected_size < standard_node_size/2:
                    expected_size = standard_node_size
                self.assertEqual(sizes[index], expected_size)
                    
            self.visualiser.set_heirarchy_view()
            self.visualiser.set_heirarchy_view()

            view = self.visualiser._builder.view
            sizes = self.visualiser.add_in_centrality_node_size()
            self.assertEqual(len(sizes), len(view.nodes))
            for index,(node,data) in enumerate(view.nodes(data=True)):
                expected_size = 1 + len(view._graph.in_edges(node))
                expected_size = int((expected_size * standard_node_size) / 2)
                if expected_size > 100:
                    expected_size = 100
                if expected_size < standard_node_size/2:
                    expected_size = standard_node_size
                self.assertEqual(sizes[index], expected_size)

        def test_out_centrality(self):
            view = self.visualiser._builder.view
            ret_val = self.visualiser.add_out_centrality_node_size()
            self.assertIsNone(ret_val)

            standard_node_size = self.visualiser._size_h._standard_node_size
            sizes = self.visualiser.add_out_centrality_node_size()
            self.assertEqual(len(sizes), len(view.nodes))
            for index,(node,data) in enumerate(view.nodes(data=True)):
                expected_size = 1 + len(view._graph.out_edges(node))
                expected_size = int((expected_size * standard_node_size) / 2)
                if expected_size > 100:
                    expected_size = 100
                if expected_size < standard_node_size/2:
                    expected_size = standard_node_size
                self.assertEqual(sizes[index], expected_size)
                    
            self.visualiser.set_heirarchy_view()
            self.visualiser.set_heirarchy_view()

            view = self.visualiser._builder.view
            sizes = self.visualiser.add_out_centrality_node_size()
            self.assertEqual(len(sizes), len(view.nodes))
            for index,(node,data) in enumerate(view.nodes(data=True)):
                expected_size = 1 + len(view._graph.out_edges(node))
                expected_size = int((expected_size * standard_node_size) / 2)
                if expected_size > 100:
                    expected_size = 100
                if expected_size < standard_node_size/2:
                    expected_size = standard_node_size
                self.assertEqual(sizes[index], expected_size)

        def test_heirarchy(self):
            pass
    
    
def _get_name(subject):
    split_subject = _split(subject)
    if len(split_subject[-1]) == 1 and split_subject[-1].isdigit():
        return split_subject[-2]
    elif len(split_subject[-1]) == 3 and _isfloat(split_subject[-1]):
        return split_subject[-2]
    else:
        return split_subject[-1]

def _split(uri):
    return re.split('#|\/|:', uri)

def _isfloat(x):
    try:
        float(x)
        return True
    except ValueError:
        return False


if __name__ == '__main__':
    unittest.main()
