from builder.builders.abstract_view import AbstractViewBuilder
from rdflib.term import URIRef

class ViewBuilder(AbstractViewBuilder):
    def __init__(self,builder):
        super().__init__(builder)

    def full(self):
        return self._builder._graph

    def heirarchy(self):
        edges = []
        node_attrs = {}
        ids = self._builder._model_graph.identifiers
        nv_protocol = ids.objects.protocol
        nv_has_container = ids.predicates.has_container
        nv_actions = ids.predicates.actions
        for c_id,c_data in [c[0] for c in self._builder.get_container()]:
            node_attrs[c_id] = c_data
            parent = self._builder.get_parent(c_id)
            assert(parent)
            p_id,p_data = parent
            p_t_id,p_t_data = self._builder.get_rdf_type(p_id)
            if p_t_data["key"] == nv_protocol:
                continue
            node_attrs[p_id] = p_data
            edge = self._build_edge_attr(nv_has_container)
            edges.append((p_id,c_id,nv_has_container,edge))

        for n,v,e in self._builder.get_actions():
            n_id,n_data = n
            v_id,v_data = v
            
            n_t_id,n_t_data = self._builder.get_rdf_type(n_id)
            if n_t_data["key"] == nv_protocol:
                continue
            node_attrs[n_id] = n_data
            for a_id,a_data in self._builder.resolve_action(v_id):
                node_attrs[a_id] = a_data
                edge = self._build_edge_attr(nv_actions)
                edges.append((n_id,a_id,nv_actions,edge))

        return self._builder.sub_graph(edges,node_attrs)

    def io_explicit(self):
        '''
        Linear flow of actions with source and destination plates encoded.
        '''
        edges = []
        node_attrs = {}
        ids = self._builder._model_graph.identifiers
        nv_source = ids.predicates.source
        nv_dest = ids.predicates.destination
        protocol = self._builder.get_protocol(True)
        if protocol is None or protocol == []:
            return self._builder.sub_graph(edges,node_attrs)
        
        protocol = protocol[0][0]
        action = self._builder.get_actions(protocol,True)
        if action is None or action == []:
            return self._builder.sub_graph(edges,node_attrs)
        
        action = action[1][0]
        actions = self._builder.resolve_action(action)
        for index,(action) in enumerate(actions):
            a_id,a_data = action
            node_attrs[a_id] = a_data
            key = "next_action"
            edge = self._build_edge_attr(key)
            if index != 0:
                edges.append((previous_action[0],a_id,key,edge))
            previous_action = action
            sources,dests = self._builder.get_io(a_id)
            for s_id,s_data in sources:
                node_attrs[s_id] = s_data
                edge = self._build_edge_attr(nv_source)
                edges.append((s_id,a_id,nv_source,edge))

            for d_id,d_data in dests:
                node_attrs[d_id] = d_data
                edge = self._build_edge_attr(nv_dest)
                edges.append((a_id,d_id,nv_dest,edge))

        return self._builder.sub_graph(edges,node_attrs)


    def io_aggregate(self):
        '''
        Linear flow of actions with source and destination plates encoded.
        '''
        edges = []
        node_attrs = {}
        ids = self._builder._model_graph.identifiers
        nv_source = ids.predicates.source
        nv_dest = ids.predicates.destination
        protocol = self._builder.get_protocol(True)
        if protocol is None or protocol == []:
            return self._builder.sub_graph(edges,node_attrs)
        
        protocol = protocol[0][0]
        action = self._builder.get_actions(protocol,True)
        if action is None or action == []:
            return self._builder.sub_graph(edges,node_attrs)
        
        action = action[1][0]
        actions = self._builder.resolve_action(action)
        max_node = self._builder.get_next_index()
        for index,(action) in enumerate(actions):
            a_id,a_data = action
            node_attrs[a_id] = a_data
            key = "next_action"
            edge = self._build_edge_attr(key)
            if index != 0:
                edges.append((previous_action[0],a_id,key,edge))
            previous_action = action
            sources,dests = self._builder.get_io(a_id)
            for s_id,s_data in sources:
                if s_id in node_attrs:
                    max_node += 1
                    s_id = max_node
                node_attrs[s_id] = s_data
                edge = self._build_edge_attr(nv_source)
                edges.append((s_id,a_id,nv_source,edge))

            for d_id,d_data in dests:
                if d_id in node_attrs:
                    max_node += 1
                    d_id = max_node
                node_attrs[d_id] = d_data
                edge = self._build_edge_attr(nv_dest)
                edges.append((a_id,d_id,nv_dest,edge))

        return self._builder.sub_graph(edges,node_attrs)
        
    def flow(self):
        edges = []
        node_attrs = {}
        protocol = self._builder.get_protocol(True)
        if protocol is None or protocol == []:
            return self._builder.sub_graph(edges,node_attrs)
        
        protocol = protocol[0][0]
        action = self._builder.get_actions(protocol,True)
        if action is None or action == []:
            return self._builder.sub_graph(edges,node_attrs)
        
        action = action[1][0]
        actions = self._builder.resolve_action(action)
        max_node = self._builder.get_next_index()
        f_actions = []
        for a_id,a_data in actions:
            if a_id in node_attrs:
                max_node += 1
                a_id = max_node
            f_actions.append((a_id,a_data))
            node_attrs[a_id] = a_data

        previous_action = f_actions[0]
        node_attrs[previous_action[0]] = previous_action[1]
        f_actions = f_actions[1:]
        for action in f_actions:
            a_id,a_data = action
            key = "next_action"
            edge = self._build_edge_attr(key)
            edges.append((previous_action[0],a_id,key,edge))
            previous_action = action

        return self._builder.sub_graph(edges,node_attrs)

    def io_implicit(self):
        edges = []
        node_attrs = {}
        protocol = self._builder.get_protocol(True)
        if protocol is None or protocol == []:
            return self._builder.sub_graph(edges,node_attrs)
        
        protocol = protocol[0][0]
        action = self._builder.get_actions(protocol,True)
        if action is None or action == []:
            return self._builder.sub_graph(edges,node_attrs)
        
        action = action[1][0]
        previous_sources = []
        actions = self._builder.resolve_action(action)
        for index,(a_id,a_data) in enumerate(actions):
            sources,dests = self._builder.get_io(a_id)
            key = a_data["key"]
            if len(sources) == 0:
                sources = previous_sources
            if len(dests) == 0 and index < len(actions) - 1:
                dests = self._builder.get_io(actions[index+1][0])[1]
            for s_id,s_data in sources:
                node_attrs[s_id] = s_data
                for d_id,d_data in dests:
                    node_attrs[d_id] = d_data
                    edge = self._build_edge_attr(key)
                    edges.append((s_id,d_id,key,edge))

            previous_sources = sources
        return self._builder.sub_graph(edges,node_attrs)