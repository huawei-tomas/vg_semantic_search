#! /usr/bin/env python
# -*- coding: utf-8

from gremlin_python import statics
from gremlin_python.structure.graph import Graph
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.strategies import *
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection

graph = Graph()
g = graph.traversal().withRemote(DriverRemoteConnection('ws://localhost:8182/gremlin','g'))

def query_for_edge(edge):
    obj1, rel, obj2 = edge
    q = g.V().\
    has("name", obj1).outE().\
has("predicate", rel).inV().\
has("name", obj2).\
values("image_id").toList()
    return q
