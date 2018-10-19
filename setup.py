#! /usr/bin/env python
# -*- coding: utf-8

import wget
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

    # make a static directory for downloading images real quick hold on
    if not os.path.exists("app/static"):
        os.mkdir("app/static")

if __name__ == "__main__":
    fetch_vg_data()
