import os

from graphs.sbol_graph import SBOLGraph
from builder.abstract_builder import AbstractBuilder
from util.sbol_identifiers import identifiers

class SBOLBuilder(AbstractBuilder):
    def __init__(self,graph):
        super().__init__()
        self._graph = SBOLGraph(graph)


    def produce_pruned_graph(self):
        final_edges = []
        node_attrs = {}
        remove_identities = []
        for n,v,k,e in self._graph.edges(keys=True,data=True):
            common_prefix_prune = False            
            for namespace in identifiers.namespaces.prune:
                if os.path.commonprefix([namespace,k[1]]) == namespace:
                    common_prefix_prune = True
                    break
            if common_prefix_prune:
                continue
            if k[1] in identifiers.predicates.prune:
                continue
            if k[1] == identifiers.predicates.rdf_type:
                if k[2] in identifiers.objects.prune:
                    remove_identities.append(n)
            node_attrs[n] = self._graph.nodes[n]
            node_attrs[v] = self._graph.nodes[v]
            final_edges.append((n,v,k,e))
        pruned_graph = self._graph.sub_graph(final_edges,node_attrs)
        for node in remove_identities:
            pruned_graph.remove_node(node)
        pruned_graph.remove_isolated_nodes()
        return pruned_graph
    
    def _get_cds(self,identity):
        cds = []
        def _get_children(parent):
            children = []
            definition = self._graph.get_definition(parent[0])
            components = self._graph.get_components(definition[0])
            if len(components) == 0:
                return [parent]
            for c in components:
                children += _get_children(c)
            return children


        for fc in self._graph.get_functional_components(identity):
            cds += _get_children(fc)
        return cds

    def produce_single_module_graph(self):
        '''
        Just dead simple single module node all components edges.
        '''
        edges,attrs = self._produce_heirachy_edges(self._graph.get_module_definitions,
                                                    self._get_cds) 
        graph = self._graph.sub_graph(edges,attrs)
        return graph

    def produce_heirarchy_graph(self):
        edges,attrs = self._produce_heirachy_edges(self._graph.get_component_definitions,
                                                    self._graph.get_components) 
        heirarchy_graph = self._graph.sub_graph(edges,attrs)
        return heirarchy_graph

    def produce_components_graph(self):
        component_edges = []
        node_attrs = {}
        type_pred = identifiers.predicates.type
        role_pred = identifiers.predicates.role
        for identity,cd in self._graph.get_component_definitions():
            for t_id,t_data in self._graph.get_types(identity):
                edge_key,edge = self._create_descriptor_edge(cd,t_data,type_pred)
                component_edges.append((identity,t_id,edge_key,edge))
                node_attrs[t_id] = t_data

            for r_id,r_data in self._graph.get_roles(identity):
                edge_key,edge = self._create_descriptor_edge(cd,r_data,role_pred)
                component_edges.append((identity,r_id,edge_key,edge))
                node_attrs[r_id] = r_data

            for c_id,c_data in self._graph.get_components(identity):
                edge_key,edge = self._create_component_edge(cd,c_data)
                component_edges.append((identity,c_id,edge_key,edge))
                node_attrs[c_id] = c_data
            node_attrs[identity] = cd

        for m_identity,md in self._graph.get_module_definitions():
            for i_id,i_data in self._graph.get_interactions(m_identity):
                edge_key,edge = self._create_descriptor_edge(md,i_data,identifiers.predicates.interaction)
                component_edges.append((m_identity,i_id,edge_key,edge))
                node_attrs[i_id] = i_data

            for fc_id,fc_data in self._graph.get_functional_components(m_identity):
                edge_key,edge = self._create_component_edge(md,fc_data)
                component_edges.append((m_identity,fc_id,edge_key,edge))
                node_attrs[fc_id] = fc_data
            node_attrs[m_identity] = md
        component_graph = self._graph.sub_graph(component_edges,node_attrs)
        return component_graph

    def produce_interaction_verbose_graph(self):
        interaction_edges = []
        node_attrs = {}
        for i_identity,i_data in self._graph.get_interactions():
            i_type_data = self._graph.get_type(i_identity)[1]
            participations = self._graph.get_participations(i_identity)
            node_attrs[i_identity] = i_data
            if len(participations) == 1:
                p_id,p_data = participations[0]
                cd = self._graph.get_component_definition(participation=p_id)
                p_type_id,p_type_data = self._graph.get_role(p_id)
                i_edge = self._create_interaction_edge(cd,cd,p_type_data,p_type_data,i_type_data,True)
                if i_edge is None:
                    continue
                interaction_edges.append(i_edge)
                node_attrs[cd[0]] = cd[1]
                continue
            
            i_type_data = i_type_data["key"]
            i_data = i_data["key"]
            for p_id,p_data in participations:
                cd1 = self._graph.get_component_definition(participation=p_id)
                p_type = self._graph.get_role(p_id)[1]["key"]
                node_attrs[cd1[0]] = cd1[1]
                try:
                    paricipation_name = identifiers.external.inhibition_participants[p_type]
                except KeyError:
                    paricipation_name = self.graph._get_name(p_type)
                try:
                    p1_dir = identifiers.external.interaction_direction[p_type]
                except KeyError:
                    p1_dir = "in"

                if p1_dir == "in":
                    edge_key = (cd1[1]["key"],i_type_data,i_data)
                    in_node = cd1[0]
                    out_node = i_identity
                else:
                    edge_key = (i_data,i_type_data,cd1[1]["key"])
                    out_node = cd1[0]
                    in_node = i_identity

                edge = {"weight": 1,"display_name" : paricipation_name}
                interaction_edges.append((in_node,out_node,edge_key,edge))
        interaction_graph = self._graph.sub_graph(interaction_edges,node_attrs)
        return interaction_graph

    def produce_interaction_graph(self):
        interaction_edges = []
        node_attrs = {}
        for i_identity,i_data in self._graph.get_interactions():
            i_type_id,i_type_data = self._graph.get_type(i_identity)
            participations = self._graph.get_participations(i_identity)
            if len(participations) == 1:
                p_id,p_data = participations[0]
                cd = self._graph.get_component_definition(participation=p_id)
                p_type_id,p_type_data = self._graph.get_role(p_id)
                i_edge = self._create_interaction_edge(cd,cd,p_type_data,p_type_data,i_type_data,False)
                if i_edge is None:
                    continue
                interaction_edges.append(i_edge)
                node_attrs[cd[0]] = cd[1]
                continue
            
            seen_combinations = []
            for p_id,p_data in participations:
                cd1 = self._graph.get_component_definition(participation=p_id)
                p1_type_id,p1_type_data = self._graph.get_role(p_id)
                node_attrs[cd1[0]] = cd1[1]
                for p2_id,p2_data in participations:
                    if p2_id == p_id:
                        continue
                    if {p_id,p2_id} in seen_combinations:
                        continue
                    
                    p2_type_id,p2_type_data = self._graph.get_role(p2_id)
                    cd2 = self._graph.get_component_definition(participation=p2_id)
                    i_edge = self._create_interaction_edge(cd1,cd2,
                            p1_type_data,p2_type_data,i_type_data)
                    if i_edge is None:
                        continue
                    seen_combinations.append({p_id,p2_id})
                    interaction_edges.append(i_edge)
                    node_attrs[cd2[0]] = cd2[1]

        interaction_graph = self._graph.sub_graph(interaction_edges,node_attrs)
        return interaction_graph

    def produce_genetic_interaction_graph(self):
        dna = [identifiers.external.component_definition_DNA,
               identifiers.external.component_definition_DNARegion]
        return self._produce_interaction_sub_graph(dna,use_last=True)

    def produce_protein_protein_interaction_graph(self):
        protein = [identifiers.external.component_definition_protein]
        accepted_interaction_types = [identifiers.external.interaction_inhibition,
                                      identifiers.external.interaction_stimulation]
        return self._produce_interaction_sub_graph(protein,interaction_types=accepted_interaction_types)

    def produce_module_graph(self):
        edges,attrs = self._produce_heirachy_edges(self._graph.get_module_definitions,
                                            self._graph.get_modules) 
        module_graph = self._graph.sub_graph(edges,attrs)
        return module_graph
                                              
    def produce_maps_graph(self):
        h_edges,h_attrs = self._produce_heirachy_edges(self._graph.get_component_definitions,self._graph.get_components)
        m_edges,m_attrs = self._produce_heirachy_edges(self._graph.get_module_definitions,self._graph.get_modules)
        node_attrs = {}
        node_attrs.update(h_attrs)
        node_attrs.update(m_attrs)
        map_edges = h_edges + m_edges
        map_graph = self._graph.sub_graph(map_edges,node_attrs)
        to_merge = []
        for identity,data in self._graph.get_module_definitions(): 
            for fc_id,fc_data in self._graph.get_functional_components(identity):
                key = (data["key"],identifiers.predicates.functional_component,fc_data["key"])
                map_graph.add_edge(identity,fc_id,key=key,weight=1,
                                display_name="functional-component")
                map_graph.set_node_attr(fc_id,fc_data)
            
            
            for module_id,module_data in self._graph.get_modules(identity):
                for map_id,map_data in self._graph.get_maps_to(module_id):
                    map_local = self._graph.get_property(map_id,identifiers.predicates.local)
                    map_remote = self._graph.get_property(map_id,identifiers.predicates.remote)
                    if len(map_local) != 1 or len(map_remote) != 1:
                        continue
                    map_local_id,map_local_data = map_local[0]
                    map_remote_id,map_remote_data = map_remote[0]
                    to_merge.append((map_local_id,map_remote_id))
            map_graph.set_node_attr(identity,data)

        for index,(n,v) in enumerate(to_merge):
            # Checks if the master none (n) has already 
            # been merged in a previous iteration.
            for m in to_merge[0:index]:
                if m[1] == n:
                    n = m[0]
            map_graph.merge_nodes(n,v)
        return map_graph



    def _produce_interaction_sub_graph(self,predicates,interaction_types=[],use_last=False):
        i_edges = []
        node_attrs = {}
        interaction_graph = self.produce_interaction_graph()
        for n1,n2,edge in interaction_graph.edges:
            n1_type = self._graph.get_type(n1)
            if n1_type is None or n1_type[1]["key"] not in predicates :
                continue
            n1_data = interaction_graph.nodes[n1]
            interaction_type = edge[1]

            n2s = self._find_nearest_interaction(n2,interaction_graph,predicates,
                                                interaction_type,interaction_types)
            if n2s is None:
                continue
            for n2,i_type in n2s:
                if use_last:
                    interaction_type = i_type
                if i_type in interaction_types:
                    interaction_type = i_type
                n2_data = interaction_graph.nodes[n2]
                node_attrs[n1] = n1_data
                node_attrs[n2] = n2_data
                try:
                    i_name = identifiers.external.interaction_type_names[interaction_type]
                except KeyError:
                    i_name = "Unknown"

                edge_key = (n1_data["key"],interaction_type,n2_data["key"])
                new_edge = {'weight': 1, 'display_name': i_name}
                i_edges.append((n1,n2,edge_key,new_edge))
        i_graph = self._graph.sub_graph(i_edges,node_attrs=node_attrs)
        return i_graph

    def _find_nearest_interaction(self,node,graph,predicates,
                    interaction_type,desired_interactions=[]):
        node_type = self._graph.get_type(node)
        if node_type is None:
            return None
        if node_type[1]["key"] in predicates:
            return [(node,interaction_type)]
        else: 
            end_nodes = []
            for n,v,e in graph.edges(node,keys=True):
                if interaction_type not in desired_interactions:
                    interaction_type = e[1]
                if n == v:
                    continue
                end_node = self._find_nearest_interaction(v,graph,predicates,
                                        interaction_type,desired_interactions)
                if end_node is not None: 
                    end_nodes += end_node
            return end_nodes

    def _find_nearest_object(self,node,graph,objects):
        node_type = self._graph.get_rdf_type(node)
        if node_type is not None:
            if node_type[1]["key"] in objects:
                return node
        for n,v,e in graph.in_edges(node,keys=True):
            if n == v: continue
            end_node = self._find_nearest_object(n,graph,objects)
            if end_node is not None:
                return end_node
        return end_nodes

    def _create_interaction_edge(self,cd1,cd2,p1_type,p2_type,i_type,allow_multi_in=False):
        cd1_id = cd1[1]["key"]
        cd2_id = cd2[1]["key"]
        cd1 = cd1[0]
        cd2 = cd2[0]
        p1_type = p1_type["key"]
        p2_type = p2_type["key"]
        i_type = i_type["key"]
        try:
            i_type_name = identifiers.external.interaction_type_names[i_type]
        except KeyError:
            i_type_name = self.graph._get_name(i_type)
        try:
            p1_dir = identifiers.external.interaction_direction[p1_type]
        except KeyError:
            p1_dir = "in"
        try:
            p2_dir = identifiers.external.interaction_direction[p2_type]
        except KeyError:
            p2_dir = "out"

        if p1_dir == "in" and p2_dir == "out":
            in_node = cd1
            in_node_id = cd1_id
            out_node = cd2
            out_node_id = cd2_id
        elif p2_dir == "in" and p1_dir == "out":
            in_node = cd2
            in_node_id = cd2_id
            out_node = cd1
            out_node_id = cd1_id
        elif p1_dir == "in" and p2_dir == "in":
            if not allow_multi_in:
                return None
            in_node = cd1
            in_node_id = cd1_id
            out_node = cd2
            out_node_id = cd2_id
        
        edge_key = (in_node_id,i_type,out_node_id)
        edge = {"weight"       : 1,
                "display_name" : i_type_name}
        return (in_node,out_node,edge_key,edge)

    def _create_descriptor_edge(self,entity,descriptor,predicate):
        edge_key = (entity["key"],predicate,descriptor["key"])
        edge = {"weight"  : 1,
                "display_name" : self._graph._get_name(predicate)}
        return edge_key,edge
        
    def _create_component_edge(self,cd,component):
        edge_key = (cd["key"],identifiers.predicates.component,component["key"])
        edge = {"weight"  : 1,
                "display_name" : "sub-component"}
        return edge_key,edge

    def _produce_heirachy_edges(self,top_level_func,sub_func):
        edges = []
        node_attrs = {}
        for identity,data in top_level_func():
            components = sub_func(identity)
            components = [self._graph.get_definition(c[0]) for c in components]
            for c_identity,component in components:
                edge_key,edge = self._create_component_edge(data,component)
                edges.append((identity,c_identity,edge_key,edge))
                node_attrs[c_identity] = component
            node_attrs[identity] = data
        return edges,node_attrs
 