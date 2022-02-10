import re
from visual.handlers.abstract_color import AbstractNodeColorHandler
from visual.handlers.abstract_color import AbstractEdgeColorHandler

class ColorHandler():
    def __init__(self,builder):
        self.node = self.NodeColorHandler(builder)
        self.edge = self.EdgeColorHandler(builder)

    class NodeColorHandler(AbstractNodeColorHandler):
        def __init__(self,builder):
            super().__init__(builder)

        def nv_type(self):
            colors = []
            col_map = {None : {"No_Role" : self._color_picker[0]}}
            col_index = len(col_map)
            for n in self._builder.v_nodes():
                rdf_type = self._builder.get_rdf_type(n)
                if rdf_type is None:
                    colors.append(col_map[None])
                else:
                    name = _get_name(rdf_type[1]["key"])
                    if name not in col_map.keys():
                        col_map[name] = self._color_picker[col_index]
                        col_index += 1
                    colors.append({name : col_map[name]})
            return colors

        def parent(self):
            colors = []
            col_map = {None : {"No-Parent" : self._color_picker[0]}}
            col_index = len(col_map)
            for n,n_data in self._builder.v_nodes(data=True):
                parent = self._builder.get_parent(n)
                if not parent:
                    colors.append(col_map[None])
                    continue
                parent_name = _get_name(parent[1]["key"])
                if parent_name not in col_map.keys():
                    col_map[parent_name] = self._color_picker[col_index]
                    col_index += 1
                colors.append({parent_name : col_map[parent_name]})
            return colors

    class EdgeColorHandler(AbstractEdgeColorHandler):
        def __init__(self,builder):
            super().__init__(builder)

        def object_type(self):
            colors = []
            col_map = {None : {"No-Type" : self._color_picker[0]}}
            col_index = 0
            for n,v,k in self._builder.v_edges(keys=True):
                code = self._builder.get_object_code(k)
                if not code:
                    colors.append(col_map[None])
                    continue
                rdf_type = self._builder.get_rdf_type(code)
                if not rdf_type:
                    colors.append(col_map[None])
                    continue
                
                rdf_type_name = _get_name(rdf_type[1]["key"])
                if rdf_type_name not in col_map.keys():
                    col_map[rdf_type_name] = self._color_picker[col_index]
                    col_index +=1
                colors.append({_get_name(rdf_type[1]["key"]):col_map[rdf_type_name]})
            return colors


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