from rdflib import RDF, RDFS, URIRef, DC, BNode,Literal
import os
import re
import networkx as nx
from opentrons.simulate import simulate
from opentrons.protocol_api.labware import Well, Location
from converters.utility import map_to_nv, get_name

accepted_file_types = ['py',"ot2"]


def convert(filename, model):
    graph = nx.MultiDiGraph()
    model_roots = model.get_base_class()
    node_count = 1
    node_map = {}
    properties = {}

    def _add_node(entity, node_count):
        if entity in node_map.keys():
            n_key = node_map[entity]
        else:
            n_key = node_count
            node_map[entity] = n_key
            node_count += 1
        if isinstance(entity, URIRef):
            e_type = "URI"
        elif isinstance(entity,BNode):
            e_type = "BNode"
        else:
            e_type = "Literal"
        graph.add_node(n_key, key=entity, type=e_type)
        return n_key, node_count

    protocol, objects, actions = _generalise(filename,model.identifiers)
    # Add Protocol Entity
    protocol_uri,protocol_pred,protocol_type = _build_protocol(protocol,model,model_roots)
    p_id, node_count = _add_node(protocol_uri, node_count)
    protocol_type_id, node_count = _add_node(protocol_type, node_count)
    graph = _add_edge(graph,p_id,protocol_type_id,protocol_pred)

    # Add Physical Objects
    properties[protocol_uri] = _get_properties(model,protocol_type)
    o_triples = _build_objects(objects,model,model_roots,properties)
    for s,p,o in o_triples:
        action_id, node_count = _add_node(s,node_count)
        action_obj_id, node_count =_add_node(o,node_count)
        graph = _add_edge(graph,action_id,action_obj_id,p)
            
    # Add Actions
    for s,p,o in _build_actions(protocol_uri,actions,model,objects,model_roots):
        action_id, node_count = _add_node(s,node_count)
        action_obj_id, node_count =_add_node(o,node_count)
        graph = _add_edge(graph,action_id,action_obj_id,p)
    return graph


def _build_protocol(protocol,model,roots):
    nv_role = model.identifiers.predicates.role
    nv_characteristic = model.identifiers.predicates.hasCharacteristic
    nv_conceptual_entity = model.identifiers.roles.conceptual_entity
    protocol, p_data = protocol
    p_id = _build_nv_uri(protocol, model.identifiers)
    properties = ([(nv_characteristic, nv_conceptual_entity)] +
                  [(nv_role, n) for n in p_data[nv_role]])
    p_id, rdftype, protocol_type = map_to_nv(p_id, properties, roots, model)
    return p_id,rdftype,protocol_type


def _build_objects(objects,model,roots,properties):
    nv_role = model.identifiers.predicates.role
    nv_characteristic = model.identifiers.predicates.hasCharacteristic
    nv_physical_entity = model.identifiers.roles.physical_entity
    nv_hasContainer = model.identifiers.predicates.hasContainer
    triples = []
    for s, data in objects.items():
            s = data[DC.title]
            parent = None
            if RDFS.subClassOf in data:
                parent = _build_nv_uri(data[RDFS.subClassOf], model.identifiers)
            s = _build_nv_uri(s, model.identifiers, _get_name(parent))
            o_properties = ([(nv_characteristic, nv_physical_entity)] +
                          [(nv_role, r) for r in data[nv_role]])
            s, p, o = map_to_nv(s, o_properties, roots, model)
            triples.append((s,p,o))
            if parent:
                triples.append((parent,nv_hasContainer,s))
                property_val = parent
            else:
                property_val = s
            
            # Action as Object
            for k,v in properties.items():
                for prop,class_type in v.items():
                    if o in class_type:
                        triples.append((k,prop,property_val)) 
                        break
    return triples


def _build_actions(subject,actions,model,objects,roots,action_log=[],parents=[]):
    triples = []
    nv_role = model.identifiers.predicates.role
    nv_characteristic = model.identifiers.predicates.hasCharacteristic
    nv_conceptual_entity = model.identifiers.roles.conceptual_entity
    nv_source = model.identifiers.predicates.source
    nv_dest = model.identifiers.predicates.destination
    nv_actions = model.identifiers.predicates.actions
    nv_action = model.identifiers.roles.action
    nv_volume = model.identifiers.predicates.volume
    action_ids = []
    for action in actions:
        sources = action[nv_source]
        dests = action[nv_dest]
        desc = action["text"]
        volume = action[nv_volume]
        action_uri = _build_action_uri(sources,dests,desc,
                    model.identifiers,action_log,parents)
        action_log.append(action_uri)
        action_props = ([(nv_characteristic, nv_conceptual_entity)] +
                  [(nv_role, nv_action)] +
                  [(k, v) for k, v in action.items()])
        s,p,o = map_to_nv(action_uri, action_props, roots, model)
        triples.append((s,p,o))
        action_ids.append(action_uri)

        if sources:
            for source in sources:
                s_data = objects[source]
                s = s_data[DC.title]
                if RDFS.subClassOf in s_data:
                    parent = _build_nv_uri(s_data[RDFS.subClassOf], model.identifiers)
                s = _build_nv_uri(s, model.identifiers, _get_name(parent))
                triples.append((action_uri,nv_source,s))

        if dests:
            for dest in dests:
                d_data = objects[dest]
                d = d_data[DC.title]
                if RDFS.subClassOf in d_data:
                    parent = _build_nv_uri(d_data[RDFS.subClassOf], model.identifiers)
                d = _build_nv_uri(d, model.identifiers, _get_name(parent))
                triples.append((action_uri,nv_dest,d))

        if nv_actions in action:
            p = parents + [_get_name(action_uri)]
            triples += _build_actions(action_uri,action[nv_actions],
                                    model,objects,roots,action_log,p)

        if volume:
            triples.append((action_uri,nv_volume,Literal(volume)))

    # Add action list
    cur_node = BNode()
    triples.append((subject,nv_actions,cur_node))
    for index, a_id in enumerate(action_ids):
        if index == len(action_ids) - 1:
            next_node = RDF.nil
        else:
            next_node = BNode()
        triples.append((cur_node,RDF.first,a_id))
        triples.append((cur_node,RDF.rest,next_node))
        cur_node = next_node
    return triples


def _get_properties(model,p_type):
    properties = {}
    p_type_c = model.get_class_code(p_type)
    for p, p_data in model.get_class_properties(p_type_c):
        classes = []
        r_id, r_data = model.get_range(p)
        for r, data in model.get_union(r_id):
            for r in model.resolve_union(r):
                classes.append(r[1][1]["key"])
                for d in model.get_derived(r[1][0]):
                    classes.append(d[1]["key"])
        properties[p_data["key"]] = classes
    return properties


def _generalise(filename, ids):
    protocol_file = open(filename)
    runlog, _bundle = simulate(protocol_file)
    objects = {}
    actions = []
    protocol_id = os.path.splitext(os.path.basename(filename))[0]
    protocol = [protocol_id, {ids.predicates.role: [ids.roles.protocol]}]
    for operation in runlog:
        instrument = None
        source = None
        dest = None
        location = None
        volume = None
        text = None
        level = operation["level"]
        payload = operation["payload"]
        if "instrument" in payload and instrument not in objects:
            instrument = payload["instrument"]
            instrument = instrument.name
            objects[instrument] = {ids.predicates.role: [ids.roles.instrument,
                                                         ids.roles.pipette],
                                   DC.title: instrument}
        if "location" in payload:
            location = payload["location"]
            if isinstance(location, Location):
                location = location.labware.object
            if isinstance(location, Well):
                if location.well_name not in objects:
                    dn = location.display_name
                    parent = location.parent.name
                    if isint(parent):
                        parent = str(location.parent.parent)
                    objects[dn] = {ids.predicates.role: [ids.roles.container,
                                                         ids.roles.well],
                                   RDFS.subClassOf: parent,
                                   DC.title: location.well_name}
                    objects[parent] = {ids.predicates.role: [ids.roles.container],
                                       DC.title: parent}
        if "locations" in payload:
            locations = payload["locations"]
            source = [locations[0].display_name]
            dest = [locations[1].display_name]
        if "volume" in payload:
            volume = payload["volume"]
        if "source" in payload:
            source = payload["source"]
            while isinstance(source,list):
                source = source[0]
            source = [source.display_name]
        if "dest" in payload:
            dest = payload["dest"]
            while isinstance(dest,list):
                dest = dest[-1]
            dest = [dest.display_name]    
        if "text" in payload:
            text = payload["text"]
        if not source and not dest and not location:
            continue
        
        if not source and not dest:
            location = location.display_name
            source, dest = _determine_action(text, location)
        action = {ids.predicates.source: source,
                  ids.predicates.destination: dest,
                  ids.predicates.volume: volume,
                  "text": text,
                  "level" : level}
        actions.append(action)

    protocol_file.close()

    def _manage(index):
        sub_actions = []
        while index <= len(actions) -1:
            action = actions[index]
            level = action["level"]
            del action["level"]
            if index >= len(runlog) -1 :
                next_level = level - 1
            else:
                next_level = runlog[index + 1]["level"]
            if next_level > level:
                # Start of SubAction
                sub_sub_actions,index = _manage(index + 1)
                action[ids.predicates.actions] = sub_sub_actions.copy()
            elif level > next_level:
                # Case: Sub-Actions finished
                sub_actions.append(action)
                return sub_actions,index
            
            sub_actions.append(action)
            index += 1
        return sub_actions,index

    actions = _manage(0)[0]
    return protocol, objects, actions

def _determine_action(text, name):
    '''
    Very hacky, can't find another way of 
    determining if something is being pulled or pushed.
    '''
    first = text.split()[0].lower()
    d_dict = {"picking": [[name], None],
              "dropping": [None, [name]],
              "aspirating": [[name], None],
              "dispensing": [None, [name]],
              "blowing"   : [None, [name]],
              "mixing"    : [[name],[name]],
              "transferring" : [[name],[name]]}
    return d_dict[first]


def _add_edge(graph,n,v,e):
    graph.add_edge(n,v,key=e,display_name=get_name(e),weight=1)
    return graph


def _build_action_uri(source,dest,desc,ids,action_log,parent=[]):
    action = desc.split()[0].lower()
    if source:
        assert(len(source) == 1)
        action = action + f' from {source[0]}'
    if dest:
        assert(len(dest) == 1)
        action = action + f' to {dest[0]}'
         
    uri = _build_nv_uri(action,ids,parent)
    count = 1
    while uri in action_log:
        new_action = action + "_" + str(count)
        count += 1
        uri = _build_nv_uri(new_action,ids,parent)
    return uri


def _build_nv_uri(name, identifiers, parent=None):
    blacklist_words = ["opentrons","μl","300"]
    def _r(s):
        s = s.lower()
        for b in blacklist_words:
            s = s.replace(b,"")
        s = s.replace(" ", "-")
        s = s.replace("--","-")
        return s
    if parent is None:
        return URIRef(identifiers.namespaces.nv + _r(name))
    if not isinstance(parent, list):
        parent = [parent]
    return URIRef(identifiers.namespaces.nv + "/".join([_r(p) for p in parent]) + "/" + _r(name))

def _get_name(subject):
    if not subject:
        return subject
    split_subject = _split(subject)
    if len(split_subject[-1]) == 1 and split_subject[-1].isdigit():
        return split_subject[-2]
    else:
        return split_subject[-1]

def _split(uri):
    return re.split('#|\/|:', uri)

def isint(value):
  try:
    int(value)
    return True
  except ValueError:
    return False
