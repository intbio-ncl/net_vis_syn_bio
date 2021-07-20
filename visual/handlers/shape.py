import re

class ShapeHandler:
    def __init__(self):
        self.node = self.NodeShapeHandler()
        self.edge = self.EdgeShapeHandler()


    class NodeShapeHandler:
        def __init__(self):
            self.shapes = ["circle",
                        "square",
                        "triangle",
                        "rectangle",
                        "diamond",
                        "hexagon",
                        "octagon",
                        "vee",
                        "parallelogram",
                        "roundrect",
                        "ellipse"]
        
        def adaptive(self,view,graph):
            default_shape = self.shapes[0]
            shapes = self.shapes[1:]
            node_shapes = []
            shape_map = {"no_type" : default_shape}
            counter = 0
            for node in view.nodes():
                obj_type = graph.graph.get_rdf_type(node)
                if obj_type is None:
                    shape = shape_map["no_type"]
                    obj_type = "No Type"
                else:
                    obj_type = _get_name(obj_type[1]["key"])
                    if obj_type in shape_map.keys():
                        shape = shape_map[obj_type]
                    else:
                        shape = shapes[counter]
                        shape_map[obj_type] = shape
                        if counter == len(shapes):
                            counter = 0
                        else:
                            counter = counter + 1 
                node_shapes.append({obj_type : shape})
            return node_shapes

        def circle(self,view):
            return [{"standard" : "circle"} for node in view.nodes]
            
        def square(self,view):
            return [{"standard" : "square"} for node in view.nodes]
            
        def triangle(self,view):
            return [{"standard" : "triangle"} for node in view.nodes]
            
        def rectangle(self,view):
            return [{"standard" : "rectangle"} for node in view.nodes]
            
        def diamond(self,view):
            return [{"standard" : "diamond"} for node in view.nodes]
            
        def hexagon(self,view):
            return [{"standard" : "hexagon"} for node in view.nodes]
            
        def octagon(self,view):
            return [{"standard" : "octagon"} for node in view.nodes]
            
        def vee(self,view):
            return [{"standard" : "vee"} for node in view.nodes]
            
    class EdgeShapeHandler:
        def __init__(self):
            pass

        def straight(self):
            return "straight"
        def bezier(self):
            return "bezier"
        def taxi(self):
            return "taxi"
        def unbundled_bezier(self):
            return "unbundled_bezier"
        def loop(self):
            return "loop"
        def haystack(self):
            return "haystack"
        def segments(self):
            return "segments"

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