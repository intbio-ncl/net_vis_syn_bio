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
            col_map = {None : self._color_picker[0],
                       BNode : self._color_picker[1]}
            col_index = len(col_map)
            all_classes = [c[1]["key"] for c in self._builder.get_classes()]
            for node,data in self._builder.v_nodes(data=True):
                key = data["key"]
                if isinstance(key,BNode):
                    colors.append({"BNode":col_map[BNode]})
                    continue
                if key in all_classes:
                    name = _get_name(key)
                    if name not in col_map.keys():
                        col_map[name] = self._color_picker[col_index]
                        col_index += 1
                    colors.append({name : col_map[name]})
                    continue
                colors.append({"No_Class" : col_map[None]})
            return colors
    
        def branch(self):
            colors = []
            color_map = {None : self._color_picker[0],
                        BNode : self._color_picker[1]}
            root_nodes = self._builder.get_base_class()
            color_index = 0
            all_classes = [c[1]["key"] for c in self._builder.get_classes()]

            def _get_parent(node):
                for p_node,p_data in self._builder.get_parent_classes(node):
                    if p_data["key"] in color_map.keys():
                        return p_data["key"]
                    _get_parent(p_node)

            for rn in root_nodes:
                color_map[rn[1]["key"]] = self._color_picker[color_index]
                color_index +=1
                children = self._builder.get_child_classes(rn[0])
                # As time of writing this, 
                # Model is Entity -> PhyscialEntity -> Many Children.
                if len(children) == 1:
                    children += self._builder.get_child_classes(children[0][0])

                for child in children:
                    key = child[1]["key"]
                    if key in color_map.keys():
                        continue
                    color_map[key] = self._color_picker[color_index]
                    color_index += 1
            for node,data in self._builder.v_nodes(data=True):
                key = data["key"]
                if isinstance(key,BNode):
                    colors.append({"BNode" : color_map[BNode]})
                    continue
                if key not in all_classes:
                    colors.append({"No_Class" : color_map[None]})
                    continue
                if key in color_map.keys():
                    name = _get_name(key)
                    colors.append({f'Child_of_{name}' : color_map[key]})
                    continue

                known_parent = _get_parent(node)
                name = _get_name(known_parent)
                colors.append({f'Child_of_{name}' : color_map[known_parent]})
            return colors


        def heirarchy(self):
            pass
            

    class EdgeColorHandler(AbstractEdgeColorHandler):
        def __init__(self,builder):
            super().__init__(builder)
        
        def branch(self):
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