import re
from visual.handlers.abstract_label import AbstractNodeLabelHandler , AbstractEdgeLabelHandler

class LabelHandler:
    def __init__(self,builder):
        self.node = self.NodeLabelHandler(builder)
        self.edge = self.EdgeLabelHandler(builder)
    
    class NodeLabelHandler(AbstractNodeLabelHandler):
        def __init__(self,builder):
            super().__init__(builder)

        def source_dest(self):
            node_labels = []
            nv_act = self._builder._model_graph.identifiers.objects.action
            nv_container = self._builder._model_graph.identifiers.objects.container
            for node,n_data in self._builder.v_nodes(data=True):
                rdf_type = self._builder.get_rdf_type(node)
                if not rdf_type:
                    node_labels.append(n_data["display_name"])
                    continue
                rdf_type = rdf_type[1]["key"]
                if self._builder._model_graph.is_derived(rdf_type,nv_container):
                    parent = self._builder.get_parent(node)
                    if not parent:
                        node_labels.append(n_data["display_name"])
                    else:
                        node_labels.append(parent[1]["display_name"])
                    continue
                if not self._builder._model_graph.is_derived(rdf_type,nv_act):
                    node_labels.append(n_data["display_name"])
                    continue
                source,dest = self._builder.get_io(node)
                assert(len(source) < 2)
                assert(len(dest) < 2)
                source = "".join([_get_name(s[1]["key"]) for s in source])
                dest = "".join([_get_name(d[1]["key"]) for d in dest])
                if source == "":
                    source = "None"
                if dest == "":
                    dest = "None"
                text = f'{source}{" - "}{dest}'
                node_labels.append(text)
            return node_labels

        def source_dest_explicit(self):
            node_labels = []
            nv_act = self._builder._model_graph.identifiers.objects.action
            nv_container = self._builder._model_graph.identifiers.objects.container
            for node,n_data in self._builder.v_nodes(data=True):
                rdf_type = self._builder.get_rdf_type(node)
                if not rdf_type:
                    node_labels.append(n_data["display_name"])
                    continue
                rdf_type = rdf_type[1]["key"]
                if self._builder._model_graph.is_derived(rdf_type,nv_container):
                    parent = self._builder.get_parent(node)
                    if not parent:
                        node_labels.append(n_data["display_name"])
                    else:
                        node_labels.append(parent[1]["display_name"])
                    continue
                if not self._builder._model_graph.is_derived(rdf_type,nv_act):
                    node_labels.append(n_data["display_name"])
                    continue
                source,dest = self._builder.get_io(node)
                assert(len(source) < 2)
                assert(len(dest) < 2)
                s_string = ""
                for s in source:
                    parent = self._builder.get_parent(s)
                    s_string = f'{s_string}{parent[1]["display_name"]}-{_get_name(s[1]["key"])}'
                d_string = ""
                for d in dest:
                    parent = self._builder.get_parent(d)
                    d_string = f'{s_string}{parent[1]["display_name"]}-{_get_name(d[1]["key"])}'

                if source == "":
                    source = "None"
                if dest == "":
                    dest = "None"
                text = f'{s_string}{" --- "}{d_string}'
                node_labels.append(text)
            return node_labels

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

    class EdgeLabelHandler(AbstractEdgeLabelHandler):
        def __init__(self,builder):
            super().__init__(builder)
        
        def process_type(self):
            edge_names = []
            for edge in self._builder.v_edges(data=True):
                edge_names.append(edge[2]["display_name"].split("-")[0])
            return edge_names

        def nv_type(self):
            edge_names = []
            for edge in self._builder.v_edges(data=True):
                edge_names.append(edge[2]["display_name"].split("-")[0])
            return edge_names
            

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
        