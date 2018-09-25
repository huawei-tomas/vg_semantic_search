#! /usr/bin/env python
# -*- coding: utf-8
from gremlin_python import statics
from gremlin_python.structure.graph import Graph
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.strategies import *
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from visualize_data import visualize_image



def query_for_edge(g, edge):
    obj1, rel, obj2 = edge
    q = g.V().\
    has("name", obj1).outE().\
has("predicate", rel).inV().\
has("name", obj2).\
values("image_id").toList()
    return q

def get_graph():
    graph = Graph()
    return graph.traversal().withRemote(DriverRemoteConnection('ws://localhost:8182/gremlin','g'))

def get_results_for_edge(g, edge):
    q = query_for_edge(g, edge)
    fnames = []
    for x in q:
        try:
            fnames.append(visualize_image(x, edges=[edge]))
        except:
            print("God Fucking dammit.")
    print(edge)
    print(q)
    fnames = [fname.split('/')[-1] for fname in fnames]
    return fnames
