import unittest
import os
import sys
import re

from rdflib import BNode,OWL
sys.path.insert(0, os.path.join(".."))
sys.path.insert(0, os.path.join("..",".."))
from visual.handlers.color_producer import ColorPicker
from visual.model import ModelVisual

curr_dir = os.path.dirname(os.path.realpath(__file__))
model_fn = os.path.join(curr_dir,"..","..","utility","nv_model.xml")



class TestPresets(unittest.TestCase):
    def setUp(self):
        self.visual = ModelVisual(model_fn)

    def tearDown(self):
        pass
    
    def test_hierarchy(self):
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
            self._color_list = ColorPicker()

        def tearDown(self):
            pass

        def test_standard(self):
            view = self.visual._builder.view
            colors = self.visual.add_standard_node_color()
            self.assertEqual(len(colors), len(view.nodes))
            for index,(node,data) in enumerate(view.nodes(data=True)):
                self.assertEqual(colors[index], {"standard" : self._color_list[0]})

            self.visual.set_hierarchy_view()
            self.visual.set_hierarchy_view()
            view = self.visual._builder.view
            colors = self.visual.add_standard_node_color()
            self.assertEqual(len(colors), len(view.nodes))
            for index,(node,data) in enumerate(view.nodes(data=True)):
                self.assertEqual(colors[index], {"standard" : self._color_list[0]})

        def test_rdf_type(self):
            view = self.visual._builder.view
            ret_val = self.visual.add_rdf_type_node_color()
            self.assertIsNone(ret_val)

            colors = self.visual.add_rdf_type_node_color()
            self.assertEqual(len(colors), len(view.nodes))
            for index,(node,data) in enumerate(view.nodes(data=True)):
                if self.visual._builder.get_rdf_type(node) is None:
                    self.assertEqual(colors[index], {"no_type" : self._color_list[1]} )
                else:
                    self.assertEqual(colors[index], {"rdf_type" :  self._color_list[0]} )


            self.visual.set_hierarchy_view()
            self.visual.set_hierarchy_view()
            view = self.visual._builder.view
            colors = self.visual.add_rdf_type_node_color()
            self.assertEqual(len(colors), len(view.nodes))
            for index,(node,data) in enumerate(view.nodes(data=True)):
                if self.visual._builder.get_rdf_type(node) is None:
                    self.assertEqual(colors[index], {"no_type" :  self._color_list[1]} )
                else:
                    self.assertEqual(colors[index], {"rdf_type" :  self._color_list[0]} )

        def test_class(self):
            view = self.visual._builder.view
            ret_val = self.visual.add_class_node_color()
            self.assertIsNone(ret_val)
            def _run_tests():    
                colors = self.visual.add_class_node_color()
                c_pass,message = _test_color_map(colors)
                self.assertEqual(c_pass,1,message)
                self.assertEqual(len(colors), len(view.nodes))
                all_classes = [c[1]["key"] for c in self.visual._builder.get_classes()]
                for index,(node,data) in enumerate(view.nodes(data=True)):
                    if isinstance(data["key"],BNode):
                        self.assertEqual(colors[index], {"BNode" :  self._color_list[1]} )
                    elif data["key"] not in all_classes:
                        self.assertEqual(colors[index], {"No_Class" : self._color_list[0]} )
                    else:
                        color = colors[index]
                        key = list(color.keys())[0]
                        val = list(color.values())[0]
                        self.assertIn(key,data["key"])
                        self.assertIn(val,self._color_list)

            _run_tests()
            self.visual.set_hierarchy_view()
            self.visual.set_hierarchy_view()
            view = self.visual._builder.view
            _run_tests()

        def test_branch(self):
            view = self.visual._builder.view
            ret_val = self.visual.add_branch_node_color()
            self.assertIsNone(ret_val)
            def _run_tests():
                colors = self.visual.add_branch_node_color()
                c_pass,message = _test_color_map(colors,False)
                self.assertEqual(c_pass,1,message)

                self.assertEqual(len(colors), len(view.nodes))
                all_classes = [c[1]["key"] for c in self.visual._builder.get_classes()]
                for index,(node,data) in enumerate(view.nodes(data=True)):
                    if isinstance(data["key"],BNode):
                        self.assertEqual(colors[index], {"BNode" :  self._color_list[1]} )
                    elif data["key"] not in all_classes and len(view.in_edges(node)) == 0:
                        self.assertEqual(colors[index], {"No_Class" : self._color_list[0]} )
                    else:
                        color = colors[index]
                        key = list(color.keys())[0]
                        val = list(color.values())[0]
                        self.assertIn(val,self._color_list)

            _run_tests()
            self.visual.set_hierarchy_view()
            self.visual.set_hierarchy_view()
            view = self.visual._builder.view
            _run_tests()

        def test_hierarchy(self):
            view = self.visual._builder.view
            ret_val = self.visual.add_hierarchy_node_color()
            self.assertIsNone(ret_val)
            def _run_tests():
                colors = self.visual.add_hierarchy_node_color()
                c_pass,message = _test_color_map(colors,False)
                self.assertEqual(c_pass,1,message)

                self.assertEqual(len(colors), len(view.nodes))
                all_classes_ids = [c[0] for c in self.visual._builder.get_classes(False)]
                all_classes = [c[1]["key"] for c in self.visual._builder.get_classes(False)]
                for index,(node,data) in enumerate(view.nodes(data=True)):
                    if data["key"] not in all_classes:
                        if any(x in [c[0] for c in view.in_edges(node)] for x in all_classes_ids):
                            color = colors[index]
                            key = list(color.keys())[0]
                            val = list(color.values())[0]
                            self.assertIn(val,self._color_list)
                        else:
                            self.assertEqual(colors[index], {"Non-Hierarchical" : self._color_list[0]} )
                    else:
                        color = colors[index]
                        key = list(color.keys())[0]
                        val = list(color.values())[0]
                        self.assertIn(val,self._color_list)
                        actual_depth = self.visual._builder.get_class_depth(node)
                        expected_depth = int(key.split("-")[1])
                        self.assertEqual(expected_depth,actual_depth)
            _run_tests()
            self.visual.set_hierarchy_view()
            self.visual.set_hierarchy_view()
            view = self.visual._builder.view
            _run_tests()
        
    class TestEdge(unittest.TestCase):
        def setUp(self):
            self.visual = ModelVisual(model_fn)
            self._color_list = ColorPicker()

        def tearDown(self):
            pass
        
        def test_standard(self):
            view = self.visual._builder.view
            colors = self.visual.add_standard_edge_color()
            self.assertEqual(len(colors), len(view.edges))
            for index,(n,v,data) in enumerate(view.edges(data=True)):
                self.assertEqual(colors[index], {"standard" : "#888"})

            self.visual.set_hierarchy_view()
            self.visual.set_hierarchy_view()
            view = self.visual._builder.view
            colors = self.visual.add_standard_edge_color()
            self.assertEqual(len(colors), len(view.edges))
            for index,(n,v,data) in enumerate(view.edges(data=True)):
                self.assertEqual(colors[index], {"standard" : "#888"})

        def test_type(self):
            view = self.visual._builder.view
            ret_val = self.visual.add_type_edge_color()
            self.assertIsNone(ret_val)
            
            view = self.visual._builder.view
            def _run_tests():
                colors = self.visual.add_type_edge_color()
                self.assertEqual(len(colors), len(view.edges))
                c_pass,message = _test_color_map(colors)
                self.assertEqual(c_pass,1,message)
            _run_tests()
            self.visual.set_hierarchy_view()
            self.visual.set_hierarchy_view()
            view = self.visual._builder.view
            _run_tests()

        def test_branch(self):
            view = self.visual._builder.view
            ret_val = self.visual.add_branch_edge_color()
            self.assertIsNone(ret_val)
            
            view = self.visual._builder.view
            def _run_tests():
                colors = self.visual.add_branch_edge_color()
                self.assertEqual(len(colors), len(view.edges))
                all_classes = [c[1]["key"] for c in self.visual._builder.get_classes()]
                c_pass,message = _test_color_map(colors,False)
                self.assertEqual(c_pass,1,message)

                for index,(n,v,k) in enumerate(view.edges(keys=True)):
                    n_data = view.nodes[n]
                    if isinstance(n_data["key"],BNode):
                        self.assertEqual(colors[index], {"BNode" :  self._color_list[1]} )
                    elif n_data["key"] not in all_classes and len(view.in_edges(n)) == 0:
                        self.assertEqual(colors[index], {"No_Class" : self._color_list[0]} )
                    else:
                        color = colors[index]
                        key = list(color.keys())[0]
                        val = list(color.values())[0]
                        self.assertIn(val,self._color_list)
            _run_tests()
            self.visual.set_hierarchy_view()
            self.visual.set_hierarchy_view()
            view = self.visual._builder.view
            _run_tests()

        def test_hierarchy(self):
            view = self.visual._builder.view
            ret_val = self.visual.add_hierarchy_edge_color()
            self.assertIsNone(ret_val)
            
            view = self.visual._builder.view
            def _run_tests():
                colors = self.visual.add_hierarchy_edge_color()
                self.assertEqual(len(colors), len(view.edges))
                all_classes_ids = [c[0] for c in self.visual._builder.get_classes(False)]
                all_classes = [c[1]["key"] for c in self.visual._builder.get_classes(False)]
                c_pass,message = _test_color_map(colors,False)
                self.assertEqual(c_pass,1,message)

                for index,(n,v,k) in enumerate(view.edges(keys=True)):
                    n_data = view.nodes[n]
                    if n_data["key"] not in all_classes:
                        if any(x in [c[0] for c in view.in_edges(n)] for x in all_classes_ids):
                            color = colors[index]
                            key = list(color.keys())[0]
                            val = list(color.values())[0]
                            self.assertIn(val,self._color_list)
                        else:
                            self.assertEqual(colors[index], {"Non-Hierarchical" : self._color_list[0]} )
                    else:
                        color = colors[index]
                        key = list(color.keys())[0]
                        val = list(color.values())[0]
                        self.assertIn(val,self._color_list)
                        actual_depth = self.visual._builder.get_class_depth(n)
                        expected_depth = int(key.split("-")[1])
                        self.assertEqual(expected_depth,actual_depth)
            _run_tests()
            self.visual.set_hierarchy_view()
            self.visual.set_hierarchy_view()
            view = self.visual._builder.view
            _run_tests()

class TestShape(unittest.TestCase):
    class TestNode(unittest.TestCase):
        def setUp(self):
            self.visual = ModelVisual(model_fn)
            
        def test_logical(self):
            view = self.visual._builder.view
            ret_val = self.visual.add_logic_node_shape()
            self.assertIsNone(ret_val)
            def _run_tests():    
                colors = self.visual.add_logic_node_shape()
                for index,(n,data) in enumerate(view.nodes(data=True)):
                    if data["key"] == OWL.intersectionOf:
                        self.assertEqual({"AND" : "rectangle"},colors[index])
                    elif data["key"] == OWL.unionOf:
                        self.assertEqual({"OR" : "triangle"},colors[index])
                    else:
                        self.assertEqual({"not_logical" : "circle"},colors[index])
            _run_tests()
            self.visual.set_requirements_view()
            self.visual.set_requirements_view()
            view = self.visual._builder.view
            _run_tests()
    
class TestSize(unittest.TestCase):
    def setUp(self):
        self.visual = ModelVisual(model_fn)
        self.builder = self.visual._builder
        self.standard_node_size = self.visual._size_h._standard_node_size

    def tearDown(self):
        pass

    def test_hierarchy(self):
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


def _test_color_map(colors,unique_keys=True):
    for color in colors:
        key = list(color.keys())[0]
        val = list(color.values())[0]
        for c in colors:
            try:
                if c[key] != val:
                    return -1,f'{c[key]} != {val}'
            except KeyError:
                if unique_keys and list(c.values())[0] == val:
                    return -1, f'{list(c.values())[0]} == {val}'
        return 1,""

if __name__ == '__main__':
    unittest.main()
