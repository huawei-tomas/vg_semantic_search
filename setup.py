#! /usr/bin/env python
# -*- coding: utf-8

import zipfile
import os
import shutil
import subprocess

def fetch_vg_data():
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

def subproc_wget(url):
    p = subprocess.Popen("wget {}".format(url), shell=True)
    p.communicate()
    fname = url.split('/')[-1]
    return fname

def setup_tinkerpop():
    urls = [
            "http://mirrors.ocf.berkeley.edu/apache/tinkerpop/3.3.3/apache-tinkerpop-gremlin-server-3.3.3-bin.zip",
            "https://www.dropbox.com/s/nbu3wmmoop0iykz/vg-scene-graph-minimal.graphml"
           ]
    os.mkdir("tmp")
    os.chdir("tmp")
    
    fnames = []
    for url in urls:
        print("downloading {}".format(url))
        fnames.append(subproc_wget(url))

    # Extract tinkerpop server one directory up.
    zfile = zipfile.ZipFile(fnames[0], 'r')
    zfile.extractall("..")

    # Move the graphml where it needs to be
    tinkerpop_dir = "apache-tinkerpop-gremlin-server-3.3.3"
    graphml_fname = "vg-scene-graph-minimal.graphml"
    shutil.copy(graphml_fname, "../{}/data".format(tinkerpop_dir))

    # Clean it up.
    os.chdir("..")
    shutil.rmtree("./tmp")

    # Now let's move the config file
    server_conf = "gremlin-server-vg-scene-graph.yaml"
    shutil.copy(
        "./tinkerpop/{}".format(server_conf),
        "./{}/conf/{}".format(tinkerpop_dir, server_conf)
    )

    # Time for the script to move.
    groovy_script = "load-vg-scene-graph.groovy"
    shutil.copy(
        "./tinkerpop/{}".format(groovy_script),
        "./{}/scripts/{}".format(tinkerpop_dir, groovy_script)
    )

    # We allowed tinkerpop to use more memory. Copy it over there.
    server_fname = "gremlin-server.sh"
    # Pretty sure shutil would just copy over, but w/e not gonna bother to test.
    rel_server_fname = "./{}/bin/{}".format(tinkerpop_dir, server_fname)
    os.remove(rel_server_fname)
    shutil.copy(
        "./tinkerpop/{}".format(server_fname),
        rel_server_fname
    )

    # Make it executable
    p = subprocess.Popen("chmod +x {}".format(rel_server_fname), shell=True)
    p.communicate()

    # make a static directory for downloading images real quick hold on
    os.mkdir("app/static")

if __name__ == "__main__":
    fetch_vg_data()
    setup_tinkerpop()
