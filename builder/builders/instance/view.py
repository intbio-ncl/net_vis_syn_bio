import re

from rdflib.term import URIRef

class ViewBuilder:
    def __init__(self,builder):
        self._builder = builder

    def full(self):
        return self._builder._graph

    def pruned(self):
        edges = []
        node_attrs = {}
        w_predicates = self._builder._model_graph.identifiers.predicates
        for n,v,k,e in self._builder.edges(keys=True,data=True):
            if k not in w_predicates:
                continue
            node_attrs[n] = self._builder.nodes[n]
            node_attrs[v] = self._builder.nodes[v]
            edges.append((n,v,k,e))
        return self._builder.sub_graph(edges,node_attrs)
         
    def hierarchy(self):
        edges = []
        node_attrs = {}
        for entity,data in self._builder.get_entities():
            children = self._builder.get_children(entity)
            if len(children) == 0:
                continue
            node_attrs[entity] = data
            for child,key in children:
                child,c_data = child
                node_attrs[child] = c_data
                edge = self._build_edge_attr(key)
                edges.append((entity,child,key,edge))
        return self._builder.sub_graph(edges,node_attrs)

    def interaction_explicit(self):
        edges = []
        node_attrs = {}
        for interaction,i_type,e in self._builder.get_interaction():
            interaction,interaction_data = interaction
            consistsOf = self._builder.get_consistsof(interaction,True)
            if consistsOf == []:
                raise NotImplementedError("Not Implemented.")
                continue
            consistsOf = consistsOf[1][0]
            consistsOf = self._builder.resolve_list(consistsOf)
            inputs,outputs = self._builder.get_interaction_io(interaction)
            for index,n in enumerate(consistsOf):
                n,n_data = n
                node_attrs[n] = n_data
                if index == len(consistsOf) -1:
                    for obj,pred in outputs:
                        obj,obj_data = obj
                        node_attrs[obj] = obj_data
                        edge = self._build_edge_attr(pred)
                        edges.append((n,obj,pred,edge))
                if index == 0:
                    for obj,pred in inputs:
                        obj,obj_data = obj
                        node_attrs[obj] = obj_data
                        edge = self._build_edge_attr(pred)
                        edges.append((obj,n,pred,edge))
                    continue
                p_element = consistsOf[index-1][0]
                edges.append((p_element,n,pred,edge))
        return self._builder.sub_graph(edges,node_attrs)

    def interaction_verbose(self):
        edges = []
        node_attrs = {}
        for interaction,i_type,e in self._builder.get_interaction():
            interaction,interaction_data = interaction
            inputs,outputs = self._builder.get_interaction_io(interaction)
            for obj,pred in inputs:
                obj,obj_data = obj
                node_attrs[obj] = obj_data
                edge = self._build_edge_attr(pred)
                edges.append((obj,interaction,pred,edge))
            for obj,pred in outputs:
                obj,obj_data = obj
                node_attrs[obj] = obj_data
                edge = self._build_edge_attr(pred)
                edges.append((interaction,obj,pred,edge))
            node_attrs[interaction] = interaction_data
        return self._builder.sub_graph(edges,node_attrs)

    def interaction(self):
        edges = []
        node_attrs = {}
        for interaction,i_type,e in self._builder.get_interaction():
            interaction,interaction_data = interaction
            i_type,i_type_data = i_type
            i_type_key = i_type_data["key"]
            inputs,outputs = self._builder.get_interaction_io(interaction)
            for inp,pred in inputs:
                inp,inp_data = inp
                node_attrs[inp] = inp_data
                for out,pred in outputs:
                    out,out_data = out
                    node_attrs[out] = out_data
                    edge = self._build_edge_attr(i_type_key)
                    edges.append((inp,out,i_type_key,edge))
        return self._builder.sub_graph(edges,node_attrs)

    def interaction_genetic(self):
        edges = []
        node_attrs = {}
        i_graph = self.interaction()
        genetic_pred = self._builder._model_graph.identifiers.objects.DNA
        g_p_model_code = self._builder._model_graph.get_class_code(genetic_pred)
        for n,v,e in i_graph.edges(keys=True):
            n_data = i_graph.nodes[n]
            n_type = self._builder.get_rdf_type(n)[1]["key"]
            if not self._builder._model_graph.is_derived(n_type,g_p_model_code):
                continue
            end_nodes = self._find_nearest_interaction(n,g_p_model_code,) 

            print(n_data["key"],v_data["key"],e)
        return self._builder.sub_graph(edges,node_attrs)

    def protein_interaction(self):
        edges = []
        node_attrs = {}
        raise NotImplementedError()
        return self._builder.sub_graph(edges,node_attrs)

    def module(self):
        edges = []
        node_attrs = {}
        raise NotImplementedError()
        return self._builder.sub_graph(edges,node_attrs)

    def _find_nearest_interaction(self,node):
        pass      

    def _build_edge_attr(self,key):
        return {"display_name" : self._get_name(key)}

    def _get_name(self,subject):
        split_subject = self._split(subject)
        if len(split_subject[-1]) == 1 and split_subject[-1].isdigit():
            return split_subject[-2]
        elif len(split_subject[-1]) == 3 and _isfloat(split_subject[-1]):
            return split_subject[-2]
        else:
            return split_subject[-1]

    def _split(self,uri):
        return re.split('#|\/|:', uri)

def _isfloat(x):
    try:
        float(x)
        return True
    except ValueError:
        return False