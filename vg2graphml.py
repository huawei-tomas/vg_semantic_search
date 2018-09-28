#! /usr/bin/env python
# -*- coding: utf-8

import os
import json
import wget
import zipfile
import networkx as nx
import sys


def load_objs(obj_fname="./data/objects.json.zip"):
    """Loads objects in from a download of Visual Genome.

    Args:
        obj_fname - The filename of the zipped object JSON from Visual Genome.
    """
    if sys.version_info < (3, 0):
        with zipfile.ZipFile(obj_fname, 'r') as f:
            objs = json.loads(f.read('objects.json'))
    else:
        with zipfile.ZipFile(obj_fname, 'r') as f:
            objs = json.loads(f.read('objects.json').decode('utf8'))
    return objs

def load_rels(rel_fname="./data/relationships.json.zip"):
    """Loads relationships in from a download of Visual Genome.

    Args:
        rel_fname - The filename of the relationship object JSON from Visual Genome.
    """
    if sys.version_info < (3, 0):
        with zipfile.ZipFile(rel_fname, 'r') as f:
            rels = json.loads(f.read('relationships.json'))
    else:
        with zipfile.ZipFile(rel_fname, 'r') as f:
            rels = json.loads(f.read('relationships.json').decode('utf8'))
    return rels

def make_disambig(alias_fname):
    """Makes a disambiguation dictionary to map various labels onto a canonical label.

    Args:
        alias_fname - Filename of the alias set.

    Returns:
        disambig - Dictionary with non-canonical to canonical term mapping.
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
    """Adds nodes from the objects in visual genome.

    Args:
        G - Networkx graph to add objects to.
        objs - Object data from visual genome.
        obj_disambig - A disambiguation dictionary.
        every_nth - downsampling by only adding objects from every nth image.

    Returns:
        G - Graph with object vertices.
        junk - List of image_ids to avoid when processing edges.
    """
    junk = {}
    for k, img in enumerate(objs):
        image_id = img['image_id']
        image_url = img.get('image_url')
        if k % every_nth != 0:
            junk[image_id] = 1
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
    return G, junk

def add_rel_edges(G, rels, rel_disambig, junk):
    """
    """
    for img in rels:
        image_id = img['image_id']
        # Don't add those relationships from these images
        if image_id in junk:
            continue
        for rel in img['relationships']:
            sub_id = rel['subject']['object_id']
            obj_id = rel['object']['object_id']
            rel_id = rel['relationship_id']
            predicate = rel_disambig.get(rel['predicate'])
            G.add_edge(sub_id, obj_id, relationship_id=rel_id)
            if predicate is not None:
                G.edges[sub_id, obj_id]['predicate'] = str(predicate).lower()
                G.edges[sub_id, obj_id]['canonical_predicate'] = True
            else:
                G.edges[sub_id, obj_id]['predicate'] = str(rel['predicate']).lower()
                G.edges[sub_id, obj_id]['canonical_predicate'] = False
    return G

def conditional_histo(G):
    """
    """
    h = {}
    elist = G.edges
    for x in elist:
        obj_id1, obj_id2 = x
        obj_name1 = G.nodes[obj_id1].get('name')
        obj_name2 = G.nodes[obj_id2].get('name')
        rel_val = G.edges[x].get('predicate')
        obj1_iscanon = G.nodes[obj_id1].get('canonical_name')
        obj2_iscanon = G.nodes[obj_id2].get('canonical_name')
        rel_iscanon = G.edges[x].get('canonical_predicate')
        print(obj_name1, rel_val, obj_name2)
        if obj1_iscanon and obj2_iscanon and rel_iscanon:
            if obj_name1 not in h:
                h[obj_name1] = {rel_val:{obj_name2:1}}
            else:
                if rel_val not in h[obj_name1]:
                    h[obj_name1][rel_val] = {obj_name2:1}
                else:
                    if obj_name2 not in h[obj_name1][rel_val]:
                        h[obj_name1][rel_val][obj_name2] = 1
                    else:
                        h[obj_name1][rel_val][obj_name2] += 1
    return h

def purge_funkiness(fname):
    """
    """
    with open(fname, 'r') as f:
        in_str = f.read()

    out_str = in_str.replace('\x00','')

    with open(fname,'w') as f:
        f.write(out_str)

def main():
    """
    """
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
    G, blacklist = add_obj_nodes(G, objs, obj_disambig, every_nth=1)

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
