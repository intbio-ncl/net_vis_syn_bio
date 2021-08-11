from logging import root
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
            color_map = _init_branch_map(self)
            all_classes = [c[1]["key"] for c in self._builder.get_classes()]
            for node,data in self._builder.v_nodes(data=True):
                key = data["key"]
                if isinstance(key,BNode):
                    colors.append({"BNode" : color_map[BNode]})
                    continue
                if key not in all_classes:
                    for o in [c[0] for c in self._builder.in_edges(node)]:
                        o = self._builder.nodes[o]["key"]
                        if o in color_map.keys():   
                            name = _get_name(o)
                            colors.append({f'Child_of_{name}' : color_map[o]})
                            break
                    else:
                        colors.append({"No_Class" : color_map[None]})
                    continue
                if key in color_map.keys():
                    name = _get_name(key)
                    colors.append({f'Child_of_{name}' : color_map[key]})
                    continue
                known_parent = _get_parent(node,color_map,self._builder)
                name = _get_name(known_parent)
                colors.append({f'Child_of_{name}' : color_map[known_parent]})
            return colors

        def hierarchy(self):
            colors = []
            colors_map = _init_hierarchy_map(self)
            for n,data in self._builder.v_nodes(data=True):
                key = data["key"]
                if key not in colors_map.keys():
                    for o in [c[0] for c in self._builder.in_edges(n)]:
                        o = self._builder.nodes[o]["key"]
                        if o in colors_map.keys():
                            color,depth = colors_map[o]
                            colors.append({f'Depth-{depth}' : color})
                            break
                    else:
                        colors.append({"Non-Hierarchical" : colors_map[None]})
                else:
                    color,depth = colors_map[key]
                    colors.append({f"Depth-{depth}" : color})
            return colors
            

    class EdgeColorHandler(AbstractEdgeColorHandler):
        def __init__(self,builder):
            super().__init__(builder)
        
        def branch(self):
            colors = []
            color_map = _init_branch_map(self)
            all_classes = [c[1]["key"] for c in self._builder.get_classes()]
            for n,v,k in self._builder.v_edges(keys=True):
                n_data = self._builder.v_nodes[n]
                key = n_data["key"]
                if isinstance(key,BNode):
                    colors.append({"BNode" : color_map[BNode]})
                    continue
                if key not in all_classes:
                    for o in [c[0] for c in self._builder.in_edges(n)]:
                        o = self._builder.nodes[o]["key"]
                        if o in color_map.keys():   
                            name = _get_name(o)
                            colors.append({f'Child_of_{name}' : color_map[o]})
                            break
                    else:
                        colors.append({"No_Class" : color_map[None]})
                    continue

                if key in color_map.keys():
                    name = _get_name(key)
                    colors.append({name : color_map[key]})
                    continue
                known_parent = _get_parent(n,color_map,self._builder)
                name = _get_name(known_parent)
                colors.append({name : color_map[known_parent]})
            return colors
        
        def hierarchy(self):
            colors = []
            color_map = _init_hierarchy_map(self)
            for n,v,k in self._builder.v_edges(keys=True):
                n_data = self._builder.v_nodes[n]
                key = n_data["key"]
                if key not in color_map.keys():
                    for o in [c[0] for c in self._builder.in_edges(n)]:
                        o = self._builder.nodes[o]["key"]
                        if o in color_map.keys():
                            color,depth = color_map[o]
                            colors.append({f'Depth-{depth}' : color})
                            break
                    else:
                        colors.append({"Non-Hierarchical" : color_map[None]})
                else:
                    color,depth = color_map[key]
                    colors.append({f"Depth-{depth}" : color})
            return colors




def _get_parent(node,color_map,builder):
    for p_node,p_data in builder.get_parent_classes(node):
        if p_data["key"] in color_map.keys():
            return p_data["key"]
        _get_parent(p_node,color_map,builder)

def _init_branch_map(handler):
    color_map = {None : handler._color_picker[0],
                BNode : handler._color_picker[1]}
    root_nodes = handler._builder.get_base_class()
    color_index = 0
    for rn in root_nodes:
        color_map[rn[1]["key"]] = handler._color_picker[color_index]
        color_index +=1
        children = handler._builder.get_child_classes(rn[0])
        # As time of writing this, 
        # Model is Entity -> PhyscialEntity -> Many Children.
        if len(children) == 1:
            children += handler._builder.get_child_classes(children[0][0])
        for child in children:
            key = child[1]["key"]
            if key in color_map.keys():
                continue
            color_map[key] = handler._color_picker[color_index]
            color_index += 1
    return color_map

def _init_hierarchy_map(handler):
    # Currently root is only one node but 
    # future proofing just in case.
    root_index = 0
    colors_map = {None : handler._color_picker[0]}
    def _handle_branch(root_node,cur_col,cur_depth):
        child_color = handler._color_picker.increase_shade(cur_col)
        cur_depth +=1
        for child,data in handler._builder.get_child_classes(root_node):
            colors_map[data["key"]] = (child_color,cur_depth)
            _handle_branch(child,child_color,cur_depth)

    for rn,data in handler._builder.get_base_class():
        colors_map[data["key"]] = handler._color_picker[root_index],0
        root_color = handler._color_picker[root_index]
        _handle_branch(rn,root_color,0)
        root_index +=1
    return colors_map

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