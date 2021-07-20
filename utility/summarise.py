import sys
import re


def get_all_views(filename):
    summary_view = {} # summarise_json(graph)
    tree_view = {} #heirachy_json(graph)
    functional_view = {}# functional_json(graph)
    return summary_view,tree_view,functional_view

'''
def summarise_json(graph):
    json_summary = {}
    json_summary["Component Definitions"] = _component_definitions(graph)
    json_summary["Module Definitions"] = _module_definitions(graph)
    return json_summary


def heirachy_json(graph):
    json_heirachy = {}
    for cd in graph.get_component_definitions():
        if len(graph.get_heirachical_instances(cd)) > 0:
            continue
        types = _get_types(cd,graph)
        roles = _get_roles(cd,graph)
        name = f'{_get_name(cd)} - {"-".join(types)} - {"-".join(roles)}'
        level = _build_heirachy_tree(cd,graph)
        if len(level) > 0:
            json_heirachy[name] = level
    return json_heirachy


def functional_json(graph):
    json_functional = {}
    for md in graph.get_module_definitions():
        json_functional[_get_name(md)] = _build_functional_tree(md,graph)
    return json_functional


def _build_functional_tree(entity,graph):
    level = {}
    interactions = _get_interactions(entity,graph)
    sub_modules = {}
    for module in graph.get_heirachical_instances(entity):
        definition = graph.get_definition(module)
        sub_modules[_get_name(definition)] = _build_functional_tree(definition,graph)
    if len(interactions) > 0:
        level["Interactions"] = interactions
    if len(sub_modules) > 0:
        level["Sub Modules"] = sub_modules
    return level


def _build_heirachy_tree(entity,graph):
    level = {}
    for component in graph.get_components(entity):
        definition = graph.get_definition(component)
        level[_get_name(definition)] = _build_heirachy_tree(definition,graph)
    return level


def _component_definitions(graph):
    cd_json = {}
    for cd in graph.get_component_definitions():
        types = _get_types(cd,graph)
        roles = _get_roles(cd,graph)
        components = _get_instances(cd,graph)
        cd_name = _get_name(cd)

        cd_json[cd_name] = {}
        if len(roles) > 0:
            cd_json[cd_name]["roles"] = roles 
        if len(types) > 0:
            cd_json[cd_name]["types"] = types 
        if len(components) > 0:
            cd_json[cd_name]["components"] = components 
    return cd_json


def _get_types(identity,graph):
    types = []
    for t in graph.get_types(identity):
        try:
            type_name = identifiers.external.cd_type_names[t]
        except KeyError:
            type_name = t
        types.append(type_name)
    return types


def _get_roles(identity,graph):
    roles = []
    for r in graph.get_roles(identity):
        try:
            role_name = identifiers.external.cd_role_name[r]
        except KeyError:
            role_name = r
        roles.append(role_name)
    return roles


def _get_instances(identity,graph):
    instances = {}
    instance_parents = []
    for instance in graph.get_heirachical_instances(identity):
        instance_name = _get_name(graph.get_component_definition(instance))
        instance_parents.append(instance_name)
    
    if len(instance_parents) > 0:
        instances["Contained Within"] = instance_parents

    for instance in graph.get_functional_instances(identity):
        instance_parent = graph.get_module_definition(instance)
    return instances


def _module_definitions(graph):
    md_json = {}
    for md in graph.get_module_definitions():
        components = _get_functional_components(md,graph)
        interactions = _get_interactions(md,graph)
        md_json[_get_name(md)] = {"components" : components,"interactions" : interactions}
    return md_json


def _get_functional_components(identity,graph):
    fcs = {}
    for fc in graph.get_functional_components(identity):
        definition = graph.get_definition(fc)
        fcs[_get_name(fc)] = _get_name(definition)
    return fcs


def _get_interactions(identity,graph):
    interactions = {}
    for interaction in graph.get_interactions(md=identity):
        name = _get_name(interaction)
        for i_type in graph.get_types(interaction):
            try:
                type_name = identifiers.external.interaction_type_names[i_type]
            except KeyError:
                type_name = i_type
            name = f'{name} - {type_name}'
        interactions[name] = _get_participants(interaction,graph)
    return interactions


def _get_participants(identity,graph):
    participants = []
    for participation in graph.get_participants(interaction=identity):
        participant = graph.get_functional_components(participation=participation)
        definition = graph.get_definition(participant)

        name = _get_name(definition)
        for r in graph.get_roles(participation):
            try:
                role_name = identifiers.external.inhibition_participants[r]
            except KeyError:
                role_name = r
            name = f'{name} - {role_name}'

        participants.append(name)
    return participants


def _get_name(subject):
    split_subject = _split(subject)
    if len(split_subject[-1]) == 1 and split_subject[-1].isdigit():
        return split_subject[-2]
    else:
        return split_subject[-1]


def _split(uri):
    return re.split('#|\/|:', uri)

if __name__ == "__main__":
    summarise_json(sys.argv[1])
'''