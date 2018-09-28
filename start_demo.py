#! /usr/bin/env python
# -*- coding: utf-8

# File: start_demo.py
# Author: Thomas Wood: thomas.wood@huawei.com

import os
import time
import subprocess

def spin_tinkerpop():
    tinkerpop_dir = "apache-tinkerpop-gremlin-server-3.3.3"
    os.chdir(tinkerpop_dir)
    server_fname = "gremlin-server.sh"
    rel_server_fname = "./bin/{}".format(server_fname)

    server_conf = "gremlin-server-vg-scene-graph.yaml"
    rel_conf_fname = "./conf/{}".format(server_conf)

    server_command = "{} {} > server_log &".format(rel_server_fname, rel_conf_fname)
    print(server_command)
    p = subprocess.Popen(server_command, shell=True)
    p.communicate()
    # It takes a minute for the graphml of the visual genome to load. Wait.
    time.sleep(60)
    os.chdir("..")

def spin_demo_page():
    demo_command = "FLASK_APP=frontend.py flask run"
    p = subprocess.Popen(['gnome-terminal', '-x', demo_command], shell=True)


if __name__ == "__main__":
    spin_tinkerpop()
    spin_demo_page()
