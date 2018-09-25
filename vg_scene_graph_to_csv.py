#! /usr/bin/env python
# -*- coding: utf-8

import json
import zipfile
import time

def load_objs(obj_fname="./data/objects.json.zip"):
    """Loads objects in from a download of Visual Genome.

    Args:
        obj_fname: The filename of the zipped object JSON from Visual Genome.
    """
    with zipfile.ZipFile(obj_fname, "r") as f:
        objs = json.loads(f.read("objects.json"))
    return objs

def load_rels(rel_fname="./data/relationships.json.zip"):
    """Loads relationships in from a download of Visual Genome.

    Args:
        rel_fname: The filename of the relationship object JSON from Visual Genome.
    """
    with zipfile.ZipFile(rel_fname, "r") as f:
        rels = json.loads(f.read("relationships.json"))
    return rels

def make_disambig(alias_fname):
    """Creates a dictionary mapping non-canonical to canonical names.

    Args:
        alias_fname: The filename of the aliases.
    """
    with open(alias_fname, "r") as f:
        aliases = f.read().split("\n")[:-1]
    disambig = {}
    for x in aliases:
        y = x.split(",")
        canon = y[0].lower()
        # Map canon to canon so we don't have to check every time. Just look it up.
        disambig[canon] = canon
        term_aliases = y[1:]
        for alias in term_aliases:
            disambig[alias.lower()] = canon

    return disambig

def add_objects(objs, obj_disambig):
    """
    """
    vertices = []
    labelname_ids = {}
    unique_names = 0
    for img in objs:
        # image_id = img["image_id"]
        for obj in img["objects"]:
            # obj_id = obj["object_id"]
            name = obj["names"][0].lower()
            canon = obj_disambig.get(name)
            if canon is None:
                is_canon = 0
            else:
                is_canon = 1
                name = canon
            if name not in labelname_ids:
                unique_names += 1
                labelname_ids[name] = unique_names
            labelname_id = labelname_ids[name]
            vertices.append([labelname_id, "object", "", name, is_canon])

    return vertices

def add_relationships(rels, rel_disambig):
    """
    """
    edges = []
    for img in rels:
        image_id = img["image_id"]
        for rel in img["relationships"]:
            sub_id = rel["subject"]["object_id"]
            obj_id = rel["object"]["object_id"]
            rel_id = rel["relationship_id"]
            predicate = rel["predicate"].lower()
            canon = rel_disambig.get(predicate)
            if canon is None:
                is_canon = 0
            else:
                is_canon = 1
                predicate = canon
            edges.append([sub_id, obj_id, "relationship", rel_id, predicate, is_canon])

    return edges

def write_csv(data, fname):
    output = '\n'.join([','.join(map(str, row)) for row in data])
    with open(fname, "w") as f:
        f.write(output)

def main():
    """Main function. Load in data and create CSV for uploading to GES.
    """

    # Load objects and relationships
    t0 = time.time()
    print("loading JSON data on scene-graph nodes")
    objs = load_objs()
    t1 = time.time()
    print("took {} seconds.".format(t1 - t0))
    print("and edges")
    rels = load_rels()
    t2 = time.time()
    print("took {} seconds.".format(t2 - t1))

    # Load in aliases and make disambiguation dictionaries.
    print("making disambiguation dicts")
    obj_alias_fname = "./data/object_alias.txt"
    rel_alias_fname = "./data/relationship_alias.txt"
    obj_disambig = make_disambig(obj_alias_fname)
    rel_disambig = make_disambig(rel_alias_fname)

    t0 = time.time()
    print("making list of vertices to export to CSV")
    obj_list = add_objects(objs, obj_disambig)
    t1 = time.time()
    print("took {} seconds.".format(t1 - t0))
    print("making list of edges to export to CSV")
    rel_list = add_relationships(rels, rel_disambig)
    t2 = time.time()
    print("took {} seconds.".format(t2 - t1))


    fname_vertex = "vertex.csv"
    fname_edge = "edge.csv"

    t0 = time.time()
    print("writing out {}".format(fname_vertex))
    write_csv(obj_list, fname_vertex)
    t1 = time.time()
    print("took {} seconds.".format(t1 - t0))
    print("writing out {}".format(fname_edge))
    write_csv(rel_list, fname_edge)
    t2 = time.time()
    print("took {} seconds.".format(t2 - t1))

if __name__ == "__main__":
    main()
