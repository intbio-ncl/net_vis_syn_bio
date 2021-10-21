from rdflib import RDF,RDFS
import networkx as nx
from opentrons.simulate import simulate
from opentrons.protocol_api.labware import Well,Location

accepted_file_types = ['py']

def convert(filename,model_graph):
    graph = nx.MultiDiGraph()
    protocol_file = open(filename)
    runlog, _bundle = simulate(protocol_file)
    objects,actions =_generalise(runlog,model_graph.identifiers)

    print("\n\n") 
    for k,v in objects.items():
        print(k,v)
    print("\n")
    for action in actions:
        for k,v in action.items():
            print(k,v)
        print("\n")
    protocol_file.close()
    return graph

def _generalise(runlog,ids):
    
    objects = {}
    actions = []
    _dump(runlog)
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
            objects[instrument] = {ids.predicates.role : [ids.roles.instrument]}
        if "location" in payload:
            location = payload["location"]
            if isinstance(location,Location):
                location = location.labware.object
            if isinstance(location,Well):
                if location.well_name not in objects:
                    dn = location.display_name
                    objects[dn] = {ids.predicates.role : [ids.roles.well],
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
    name = text.split()[0].lower()
    d_dict = {"picking"    : [name,None,identifiers.roles.pick],
              "dropping"   : [None,name,identifiers.roles.drop],
              "aspirating" : [name,None,identifiers.roles.extract],
              "dispensing" : [None,name,identifiers.roles.dispense]}

    return d_dict[name]

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
