import networkx as nx
import json
from rdflib import RDF, URIRef, Literal, BNode

from converters.utility import map_to_nv, get_name

accepted_file_types = ['json']
ap_instructions = "instructions"
ap_refs = "refs"
ap_op = "op"
ap_type = "type"
ap_new = "new"
ap_object = "object"
ap_wells = "wells"
g_entities = []


def convert(filename, model):
    g_entities.clear()
    node_map = {}
    node_count = 0
    model_roots = model.get_base_class()
    graph = nx.MultiDiGraph()
    f = open(filename)
    data = json.load(f)
    f.close()

    def _add_node(entity, node_count):
        if entity in node_map.keys():
            n_key = node_map[entity]
        else:
            n_key = node_count
            node_map[entity] = n_key
            node_count += 1
        if isinstance(entity, URIRef):
            e_type = "URI"
        else:
            e_type = "Literal"
        graph.add_node(n_key, key=entity, type=e_type)
        return n_key, node_count

    triples = convert_layer(data, model, model_roots)
    for s, p, o in triples:
        action_id, node_count = _add_node(s, node_count)
        action_obj_id, node_count = _add_node(o, node_count)
        graph = _add_edge(graph, action_id, action_obj_id, p)
    return graph


def convert_layer(layer, model, roots, parent_uri=None, cur_id=None):
    triples = []
    layer = _generalise(layer)
    ids = model.identifiers
    nv_hasContainer = ids.predicates.hasContainer

    # Handle Object
    if not cur_id:
        subject, p, o = _get_object_type(layer, model, parent_uri, roots)
        triples.append((subject, p, o))
    else:
        subject = cur_id

    # Handle Physcial Entities
    containers = []
    if ap_refs in layer:
        for k, v in layer[ap_refs].items():
            c_id, c_triples, containers = _handle_physcial_entity(
                k, v, model, subject, roots, containers)
            triples += c_triples
            triples.append((parent_uri, nv_hasContainer, c_id))

    # Handle Sub Instructions
    if ap_instructions in layer:
        actions = []
        for i in layer[ap_instructions]:
            action_id, a_triples = _handle_action(
                i, model, subject, roots, containers)
            triples += a_triples
            actions.append(action_id)
            if ap_instructions in i:
                triples += convert_layer(i, model, roots, subject, action_id)

        triples += _handle_action_list(subject, actions, ids)
    return triples


def _handle_physcial_entity(name, data, model, parent, roots, containers):
    # For wells look into getting wells from model.
    triples = []
    ids = model.identifiers
    nv_role = ids.predicates.role
    nv_characteristic = ids.predicates.hasCharacteristic
    nv_name = ids.predicates.name
    nv_physical_entity = ids.roles.physical_entity
    nv_container = ids.roles.container
    nv_well = ids.roles.well
    nv_well_p = ids.predicates.well

    subject = _build_nv_uri(name, ids, parent)
    properties = [(nv_characteristic, nv_physical_entity),
                  (nv_role, nv_container)]
    if ap_new in data:
        properties.append((nv_name, Literal(data[ap_new])))

    s, p, o = map_to_nv(subject, properties, roots, model)
    triples.append((s, p, o))
    containers.append(s)
    if ap_wells in data:
        well_props = [(nv_characteristic, nv_physical_entity),
                      (nv_role, nv_well)]
        for well in data[ap_wells]:
            well_subject = _build_nv_uri(well, ids, subject, unique=False)
            ws, wp, wo = map_to_nv(well_subject, well_props, roots, model)
            triples.append((ws, wp, wo))
            triples.append((s, nv_well_p, ws))
            containers.append(ws)

    return subject, triples, containers


def _handle_action(data, model, parent, roots, containers):
    triples = []
    subject, _, container_type = _get_object_type(data, model, parent, roots)
    triples.append((subject, _, container_type))
    triples += _get_object_properties(subject,
                                      container_type, data, model, containers)
    return subject, triples


def _get_object_type(layer, model, parent, roots):
    ids = model.identifiers
    nv_role = ids.predicates.role
    nv_characteristic = ids.predicates.hasCharacteristic
    nv_conceptual_entity = ids.roles.conceptual_entity
    nv_action = ids.roles.action
    nv_protocol = ids.roles.protocol
    nv_name = ids.predicates.name

    name = layer[ap_op]
    subject = _build_nv_uri(name, ids, parent)
    properties = [(nv_characteristic, nv_conceptual_entity)]
    type_map = {
        "Protocol": nv_protocol,
        "Action": nv_action}

    assert(ap_op in layer)
    properties.append((nv_name, Literal(layer[ap_op])))
    if ap_instructions in layer:
        properties.append((nv_role, type_map[layer[ap_type]]))
    else:
        properties.append((nv_role, nv_action))
    s, p, o = map_to_nv(subject, properties, roots, model)
    return s, p, o


def _get_object_properties(subject, s_type, data, model, containers):
    triples = []
    model_code = model.get_class_code(s_type)
    for p_code, p_data in model.get_class_properties(model_code):
        predicate = p_data["key"]
        default = model.get_default_value(model_code, predicate)
        if default is not None:
            default = default[1]["key"]
            default_name = _build_nv_uri(
                default, model.identifiers, unique=False)
            triples.append((default_name, RDF.type, default))
            triples.append((subject, predicate, default_name))
            continue
        for e_code, e_data in model.get_equivalent_properties(p_code):
            e_key = str(e_data["key"])
            if e_key in data:
                obj = data[e_key]
                if isinstance(obj, str):
                    for c in containers:
                        if obj in c:
                            obj = c
                            break
                triples.append((subject, predicate, obj))
                break
    return triples


def _generalise(layer):
    '''
    Some Autoprotocol actions have unusual 
    specification that can't be automated.
    '''
    index = 0

    def _add_well(container, well):
        assert(container in refs)
        well = "w" + str(well)
        if ap_wells in refs[container]:
            refs[container][ap_wells].append(well)
        else:
            refs[container][ap_wells] = [well]
        return container + "/" + str(well)

    instructions = layer[ap_instructions]
    refs = layer[ap_refs]
    while index <= len(instructions) - 1:
        data = instructions[index]
        data_type = data[ap_op]
        new_elements = []
        if data_type == "dispense":
            columns = data["columns"]
            del data["columns"]
            for col in columns:
                new_data = data.copy()
                new_data["source"] = _add_well(
                    *new_data["reagent_source"].split("/"))
                new_data["destination"] = _add_well(
                    new_data["object"], col["column"])
                new_data["volume"] = col["volume"]
                del new_data["reagent_source"]
                new_elements.append(new_data)
        elif data_type == "thermocycle":
            groups = data["groups"]
            del data["groups"]
            for grp in groups:
                cycles = grp["cycles"]
                for step in grp["steps"]:
                    new_data = data.copy()
                    new_data.update(step.copy())
                    new_data["cycles"] = cycles
                    new_elements.append(new_data)
        elif data_type == "incubate":
            data["temperature"] = data["where"].split("_")[0] + "°C"
            del data["where"]
            new_elements.append(data)
        elif data_type == "autopick":
            groups = data["groups"]
            del data["groups"]
            for grp in groups:
                for source in grp["from"]:
                    for dest in grp["to"]:
                        new_data = data.copy()
                        new_data["source"] = _add_well(*source.split("/"))
                        new_data["destination"] = _add_well(*dest.split("/"))
                        new_elements.append(new_data)
        elif data_type == "gel_separate":
            objects = data["objects"]
            del data["objects"]
            for obj in objects:
                new_data = data.copy()
                new_data["source"] = _add_well(*obj.split("/"))
                new_elements.append(new_data)
        else:
            new_elements.append(data)

        del instructions[index]
        for d in new_elements:
            instructions.insert(index, d)
            index += 1
    layer[ap_instructions] = instructions
    return layer


def _handle_action_list(parent, actions, ids):
    triples = []
    cur_node = BNode()
    nv_actions = ids.predicates.actions
    triples.append((parent, nv_actions, cur_node))
    for index, a_id in enumerate(actions):
        if index == len(actions) - 1:
            next_node = RDF.nil
        else:
            next_node = BNode()
        triples.append((cur_node, RDF.first, a_id))
        triples.append((cur_node, RDF.rest, next_node))
        cur_node = next_node
    return triples


def _add_edge(graph, n, v, e):
    graph.add_edge(n, v, key=e, display_name=get_name(e), weight=1)
    return graph


def _build_nv_uri(name, identifiers, parent=None, unique=True):
    if parent is None:
        name = URIRef(identifiers.namespaces.nv + name.lower())
    elif isinstance(parent, list):
        name = URIRef(identifiers.namespaces.nv +
                      "/".join(parent) + "/" + str(name))
    else:
        name = URIRef(parent + "/" + name.lower())
    count = 0
    o_name = name
    if unique:
        while name in g_entities:
            name = URIRef(f'{o_name}/{count}')
            count += 1
    g_entities.append(name)
    return name
