import re

from rdflib import BNode

from visual.handlers.abstract_color import AbstractNodeColorHandler
from visual.handlers.abstract_color import AbstractEdgeColorHandler

class ColorHandler():
    def __init__(self,builder):
        self.node = self.NodeColorHandler(builder)
        self.edge = self.EdgeColorHandler(builder)

    class NodeColorHandler(AbstractNodeColorHandler):
        def __init__(self,builder):
            super().__init__(builder)

        def nv_class(self):
            colors = []
            col_map = {None : self._color_list[0],
                       BNode : self._color_list[1]}
            col_index = len(col_map)

            for node,data in self._builder.v_nodes(data=True):
                key = data["key"]
                if isinstance(key,BNode):
                    colors.append({"BNode":col_map[BNode]})
                    continue
                if key in [c[1]["key"] for c in self._builder.get_classes()]:
                    name = _get_name(key)
                    if name not in col_map.keys():
                        col_map[name] = self._color_list[col_index]
                        col_index += 1
                    colors.append({name : col_map[name]})
                    continue
                colors.append({"No Class" : col_map[None]})
            return colors


            
        def branch(self):
            pass
        def heirarchy(self):
            pass
            


    class EdgeColorHandler(AbstractEdgeColorHandler):
        def __init__(self,builder):
            super().__init__(builder)
        
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