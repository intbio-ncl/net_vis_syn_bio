from rdflib import RDF,RDFS,URIRef, OWL
import re
import networkx as nx
from opentrons.simulate import simulate
from opentrons.protocol_api.labware import Well,Location
from converters.utility import map_to_nv, get_name

accepted_file_types = ['py']

def convert(filename,model):
    graph = nx.MultiDiGraph()
    protocol_file = open(filename)
    model_roots = model.get_base_class()
    node_count = 1
    node_map = {}

    def _add_node(entity,node_count):
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
        graph.add_node(n_key, key=entity,type=e_type)
        return n_key,node_count

    runlog, _bundle = simulate(protocol_file)
    objects,actions =_generalise(runlog,model.identifiers)

    nv_role = model.identifiers.predicates.role
    nv_characteristic = model.identifiers.predicates.hasCharacteristic
    physical_entity = model.identifiers.roles.physical_entity

    for s,data in objects.items():
        s = _build_nv_uri(s,model.identifiers)
        properties = ([(nv_characteristic,physical_entity)] + 
                      [(nv_role,r) for r in data[nv_role]])
        s,p,o = map_to_nv(s,properties,model_roots,model)
        print(s,p,o)
        n,node_count = _add_node(s,node_count)
        v,node_count = _add_node(o,node_count)
        name = get_name(p)
        graph.add_edge(n,v,key=p,display_name=name,weight=1)

    '''
    for action in actions:
        for k,v in action.items():
            print(k,v)
        print("\n")
    '''
    protocol_file.close()
    return graph


def _build_nv_uri(name,identifiers):
    name = name.replace(" ","-").lower()
    return URIRef(identifiers.namespaces.nv + name)

def _generalise(runlog,ids):
    objects = {}
    actions = []
    for operation in runlog:
        instrument = None
        source = None
        destination = None
        volume = None

        level = operation["level"]
        payload = operation["payload"]
        instrument = payload["instrument"]
        instrument = instrument.name
        if instrument not in objects:
            objects[instrument] = {ids.predicates.role : [ids.roles.instrument,
                                                          ids.roles.pipette]}
        if "location" in payload:
            location = payload["location"]
            if isinstance(location,Location):
                location = location.labware.object
            if isinstance(location,Well):
                if location.well_name not in objects:
                    dn = location.display_name
                    objects[dn] = {ids.predicates.role : [ids.roles.container,ids.roles.well],
                                   RDFS.subClassOf : location.parent}

        if "locations" in payload:
            locations = payload["locations"]
        if "volume" in payload:
            volume = payload["volume"]
        if "source" in payload:
            source = payload["source"]
        if "dest" in payload:
            destination = payload["dest"]

        if source is None and destination is None:
            source,destination,action = _determine_action(payload["text"],location,ids)
        action = {"instrument" : instrument,
                  "source" : source,
                  "destination" : destination, 
                  "action":action, 
                  "volume" : volume}

        actions.append(action)
    return objects,actions

def _determine_action(text,name,identifiers):
    '''
    Very hacky, can't find another way of 
    determining if something is being pulled or pushed.
    '''
    first = text.split()[0].lower()
    d_dict = {"picking"    : [name,None,identifiers.roles.pick],
              "dropping"   : [None,name,identifiers.roles.drop],
              "aspirating" : [name,None,identifiers.roles.extract],
              "dispensing" : [None,name,identifiers.roles.dispense]}
    return d_dict[first]

def _dump(runlog):
    for operation in runlog:
        level = operation["level"]
        payload = operation["payload"]
        instrument = payload["instrument"]

        name = instrument.name
        print(name)
        if "location" in payload:
            location = payload["location"]
            print(f'Location: {location}')
            if isinstance(location,Location):
                location = location.labware.object
            if isinstance(location,Well):
                print(location.display_name)
                print(location.parent)

        if "locations" in payload:
            locations = payload["locations"]
            print(f'Locations: {locations} {type(locations)}')
        if "volume" in payload:
            volume = payload["volume"]
            print(f'Volume: {volume} {type(volume)}')
        if "source" in payload:
            source = payload["source"]
            print(f'Source: {source} {type(source)}')
        if "dest" in payload:
            dest = payload["dest"]
            print(f'Dest: {dest} {type(dest)}')
        print("\n")

