#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This script provides two files:
 - context.jsonld, that serves https://schema.lab.fiware.org/ld/fiware-datamodels-context.jsonld
 - mapping_list.yml, that serves  https://uri.fiware.org/ns/datamodels

context.jsonld is combined by extracting the properties, types and  enumerations of a JSON Schema and
converting them into terms of a JSON-LD @Context. mapping_list.yml uses the result of extracting
to prepare a list of terms with schemas and specifications.

Copyright (c) 2019 FIWARE Foundation e.V.

Authors: José M. Cantera, Dmitrii Demin
"""

import json
import yaml
import os
from datetime import datetime
from argparse import ArgumentParser

# The aggregated @context will be stored here
aggregated_context = {
}

# The list of mappings (term->schema/specification) will be stored here
terms_list = {
    "terms": {}
}

# The list of terms alerts will be stored here (if the specification file
# associated with the term doesn't exist)
alert_list = [
]

# Template to prepare a valid URL of a schema for a term mapping
schema_url = 'https://fiware.github.io/dataModels/{}'
specification_url = 'https://github.com/FIWARE/dataModels/blob/master/{}'

# Agri* schemas stored at another github organization
agri_url = 'https://github.com/GSMADeveloper/NGSI-LD-Entities/blob/master/definitions/{}.md'


def read_json(infile):
    with open(infile) as data_file:
        data = json.loads(data_file.read())

    return data


def write_json(data, outfile):
    with open(outfile, 'w') as data_file:
        data_file.write(json.dumps(data, indent=4))
        data_file.write("\n")


def write_yaml(data, outfile):
    with open(outfile, 'w') as data_file:
        data_file.write(yaml.dump(data))


# Finds a node in a JSON Schema
# (previously parsed as a Python dictionary)


def find_node(schema, node_name):
    result = None

    if isinstance(schema, list):
        for instance in schema:
            res = find_node(instance, node_name)
            if res is not None:
                result = res
                break
    elif isinstance(schema, dict):
        for member in schema:
            if member == node_name:
                result = schema[member]
                break
            else:
                res = find_node(schema[member], node_name)
                if res is not None:
                    result = res
                    break

    return result


# extracts the properties dictionary
def extract_properties(schema):
    properties = find_node(schema, 'properties')

    out = []

    if properties is None:
        return out

    for p in properties:
        if p != "type":
            out.append(p)

    return out


# extracts the entity type
def extract_entity_type(schema):
    out = None

    properties = find_node(schema, 'properties')

    if properties is not None and 'type' in properties:
        type_node = properties['type']

        if 'enum' in type_node and len(type_node['enum']) > 0:
            out = type_node['enum'][0]

    return out


# extracts the enumerations
def extract_enumerations(schema):
    out = []

    properties = find_node(schema, 'properties')

    if properties is None:
        return out

    for p in properties:
        if p != 'type':
            prop = properties[p]
            enum = find_node(prop, 'enum')
            if enum is not None:
                if isinstance(enum, list):
                    for item in enum:
                        if isinstance(item, str):
                            out.append(item)

    return out


# Generates the LD @context for a list of properties with the URI prefix
def generate_ld_context(properties, uri_prefix, predefined_mappings):
    context = {}

    if properties is None:
        return context

    for p in properties:
        if p.startswith('ref'):
            context[p] = {
                '@type': '@id',
                '@id': uri_prefix + '#' + p
            }
        elif p.startswith('date'):
            context[p] = {
                '@type': 'http://uri.etsi.org/ngsi-ld/DateTime',
                '@id': uri_prefix + '#' + p
            }
        elif p in predefined_mappings:
            context[p] = predefined_mappings[p]
        else:
            context[p] = uri_prefix + '#' + p

    return context


# Extracts from the schema the relevant JSON-LD @context
def schema_2_ld_context(schema, uri_prefix, predefined_mappings):
    properties = extract_properties(schema)
    entity_type = extract_entity_type(schema)
    enumerations = extract_enumerations(schema)

    all_properties = properties + enumerations

    ld_context = generate_ld_context(
        all_properties, uri_prefix, predefined_mappings)

    if entity_type is not None:
        ld_context[entity_type] = uri_prefix + '#' + entity_type

    return ld_context


def process_file(input_file, uri_prefix, predefined_mappings, terms_mappings):
    if os.path.isfile(input_file) and input_file.endswith('schema.json'):
        print(input_file)
        aggregate_ld_context(
            input_file,
            uri_prefix,
            predefined_mappings,
            terms_mappings)
    elif os.path.isdir(input_file):
        for f in (os.listdir(input_file)):
            process_file(os.path.join(input_file, f),
                         uri_prefix, predefined_mappings, terms_mappings)


def aggregate_ld_context(f, uri_prefix, predefined_mappings, terms_mappings):
    global aggregated_context
    global terms_list
    global alert_list

    schema = read_json(f)
    ld_context = schema_2_ld_context(schema, uri_prefix, predefined_mappings)

    for p in ld_context:
        aggregated_context[p] = ld_context[p]

        # adding related specifications and schemas
        if p not in terms_list['terms']:
            terms_list['terms'][p] = {'specifications': list(),
                                      'schemas': list()}

        terms_list['terms'][p]['schemas'].append(
            schema_url.format(f.split('../')[1]))

        file_to_add = find_file(f, terms_mappings)
        if file_to_add:
            terms_list['terms'][p]['specifications'].append(file_to_add)
        else:
            alert_list.append(f)


# Finds the specification file associated with the term
def find_file(f, terms_mappings):
    try:
        spec1 = os.path.join(f.rsplit('/', 1)[0], 'doc/spec.md')
        spec2 = os.path.join(f.rsplit('/', 1)[0], 'doc/introduction.md')
        if os.path.isfile(spec1):
            return specification_url.format(spec1.split('../')[1])
        elif os.path.isfile(spec2):
            return specification_url.format(spec2.split('../')[1])
        elif 'AgriFood' in f:
            agri_type = f.split('AgriFood/')[1].split('/schema.json')[0]
            if agri_type in terms_mappings:
                return agri_url.format(terms_mappings[agri_type])
            else:
                return None
        else:
            return None
    except UnboundLocalError:
        pass


def write_context_file():
    print('writing LD @context...' + ' size: ' + str(len(aggregated_context)))

    ld_context = {
        '@context': aggregated_context,
        'generatedAt': datetime.now().replace(microsecond=0).isoformat()
    }

    write_json(ld_context, 'context.jsonld')
    write_yaml(terms_list, 'terms_list.yml')


def main(args):
    uri_prefix = args.u

    predefined_mappings = read_json('ldcontext_mappings.json')
    terms_mappings = read_json('ldcontext_terms_mappings.json')

    process_file(args.f, uri_prefix, predefined_mappings, terms_mappings)

    write_context_file()

    print("specification file was  not found for this files")
    print("\n".join(sorted(set(alert_list))))


# Entry point
if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-f', required=True, help='folder')
    parser.add_argument('-u', required=True, help='URI prefix')

    arguments = parser.parse_args()

    main(arguments)
