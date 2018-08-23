#! /usr/bin/env python
# -*- coding: utf-8

import os
import json
import wget
import zipfile
import networkx as nx


def fetch_data():
    urls = [
            "https://visualgenome.org/static/data/dataset/objects.json.zip",
            "https://visualgenome.org/static/data/dataset/relationships.json.zip",
            "https://visualgenome.org/static/data/dataset/object_alias.txt",
            "https://visualgenome.org/static/data/dataset/relationship_alias.txt"
           ]
    if not os.path.exists('data'):
        os.mkdir('data')
    else:
        return
    os.chdir('data')
    for url in urls:
        wget.download(url)
    os.chdir('..')

def load_objs(obj_fname="./data/objects.json.zip"):
    """Loads objects in from a download of Visual Genome.

    Args:
        obj_fname: The filename of the zipped object JSON from Visual Genome.
    """
    with zipfile.ZipFile(obj_fname, 'r') as f:
        objs = json.loads(f.read('objects.json'))
    return objs

def load_rels(rel_fname="./data/relationships.json.zip"):
    """Loads relationships in from a download of Visual Genome.

    Args:
        rel_fname: The filename of the relationship object JSON from Visual Genome.
    """
    with zipfile.ZipFile(rel_fname, 'r') as f:
        rels = json.loads(f.read('relationships.json'))
    return rels

def make_disambig(alias_fname):
    """
    """
    with open(alias_fname, 'r') as f:
        aliases = f.read().split('\n')[:-1]
    disambig = {}
    for x in aliases:
        y = x.split(',')
        canon = y[0]
        # Map canon to canon so we don't have to check every time. Just look it up.
        disambig[canon] = canon
        term_aliases = y[1:]
        for alias in term_aliases:
            disambig[alias] = canon

    return disambig


def add_obj_nodes(G, objs, obj_disambig, every_nth=4):
    """
    """
    blacklist = {}
    for k, img in enumerate(objs):
        image_id = img['image_id']
        image_url = img.get('image_url')
        if k % every_nth != 0:
            blacklist[image_id] = 1
            continue
        for obj in img['objects']:
            x, y, h, w = obj['x'], obj['y'], obj['h'], obj['w']
            obj_id = obj['object_id']
            G.add_node(obj_id)
            name = obj_disambig.get(obj.get('names')[0])

            G.nodes[obj_id]['image_id'] = image_id
            G.nodes[obj_id]['x'] = x
            G.nodes[obj_id]['y'] = y
            G.nodes[obj_id]['h'] = h
            G.nodes[obj_id]['w'] = w

            if image_url is not None:
                G.nodes[obj_id]['image_url'] = image_url
            else:
                G.nodes[obj_id]['image_url'] = "None"

            if name is not None:
                G.nodes[obj_id]['name']= name
                G.nodes[obj_id]['canonical_name'] = True
            else:
                G.nodes[obj_id]['name'] = obj['names'][0]
                G.nodes[obj_id]['canonical_name'] = False
    return G, blacklist

def add_rel_edges(G, rels, rel_disambig, blacklist):
    """
    """
    for img in rels:
        image_id = img['image_id']
        if image_id in blacklist:
            continue
        for rel in img['relationships']:
            sub_id = rel['subject']['object_id']
            obj_id = rel['object']['object_id']
            rel_id = rel['relationship_id']
            predicate = rel_disambig.get(rel['predicate'])
            G.add_edge(sub_id, obj_id, relationship_id=rel_id)
            if predicate is not None:
                G.edges[sub_id, obj_id]['predicate'] = predicate
                G.edges[sub_id, obj_id]['canonical_predicate'] = True
            else:
                G.edges[sub_id, obj_id]['predicate'] = rel['predicate']
                G.edges[sub_id, obj_id]['canonical_predicate'] = False
    return G

def purge_funkiness(fname):
    with open(fname, 'r') as f:
        in_str = f.read()

    out_str = in_str.replace('\x00','')

    with open(fname,'w') as f:
        f.write(out_str)

def main():
    """
    """

    # Download object and relationship data from visual genome
    fetch_data()
    # Load objects and relationships
    print("loading JSON data on scene-graph nodes")
    objs = load_objs()
    print("and edges")
    rels = load_rels()

    # Load in aliases and make disambiguation dictionaries.
    print("making disambiguation dicts")
    obj_alias_fname = './data/object_alias.txt'
    rel_alias_fname = './data/relationship_alias.txt'
    obj_disambig = make_disambig(obj_alias_fname)
    rel_disambig = make_disambig(rel_alias_fname)

    # Make a graph to populate.
    G = nx.Graph()

    # Add object nodes
    print("adding objects as nodes")
    G, blacklist = add_obj_nodes(G, objs, obj_disambig)

    # Add edges between object nodes
    print("adding relationships as edges")
    G = add_rel_edges(G, rels, rel_disambig, blacklist)

    # Write the graph to file.
    print("writing the graph to disk")
    graphml_fname = "vg-scene-graph-minimal.graphml"
    nx.write_graphml(G, graphml_fname)

    # Purge the character encoding funkiness
    purge_funkiness(graphml_fname)

if __name__ == "__main__":
    main()
