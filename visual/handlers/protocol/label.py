import re
from visual.handlers.abstract_label import AbstractNodeLabelHandler , AbstractEdgeLabelHandler

class LabelHandler:
    def __init__(self,builder):
        self.node = self.NodeLabelHandler(builder)
        self.edge = self.EdgeLabelHandler(builder)
    
    class NodeLabelHandler(AbstractNodeLabelHandler):
        def __init__(self,builder):
            super().__init__(builder)

        def parent(self):
            node_labels = []
            nv_protocol = self._builder._model_graph.identifiers.objects.protocol
            for node,data in self._builder.v_nodes(data=True):
                parent = self._builder.get_parent(node)
                if not parent:
                    node_labels.append(data["display_name"])
                    continue
                p_rdf_type = self._builder.get_rdf_type(parent[0])
                if p_rdf_type[1]["key"] == nv_protocol:
                    node_labels.append(data["display_name"])
                    continue
                node_labels.append(_get_name(parent[1]["key"]))
            return node_labels

        def well_container(self):
            node_labels = []
            nv_well = self._builder._model_graph.identifiers.objects.well
            for node,data in self._builder.v_nodes(data=True):
                r_type = self._builder.get_rdf_type(node)
                if r_type is None:
                    node_labels.append(data["display_name"])
                    continue

                if r_type[1]["key"] == nv_well:
                    parent = self._builder.get_parent(node)
                    assert(parent)
                    node_labels.append(f'{parent[1]["display_name"]} - {data["display_name"]}')
                    continue

                node_labels.append(_get_name(data["display_name"]))
            return node_labels

    class EdgeLabelHandler(AbstractEdgeLabelHandler):
        def __init__(self,builder):
            super().__init__(builder)

        def well_container(self):
            edge_labels = []
            nv_well = self._builder._model_graph.identifiers.objects.well
            for n,v,e in self._builder.v_edges(keys=True):
                e_code = self._builder.get_object_code(e)
                try:
                    r_type = self._builder.get_rdf_type(e_code)
                except ValueError:
                    edge_labels.append(_get_name(e))
                    continue

                if r_type[1]["key"] == nv_well:
                    parent = self._builder.get_parent(e_code)
                    assert(parent)
                    edge_labels.append(f'{parent[1]["display_name"]} - {_get_name(e)}')
                    continue

                edge_labels.append(_get_name(e))
            return edge_labels
        
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
        