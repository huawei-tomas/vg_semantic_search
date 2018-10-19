#! /usr/bin/env python
# -*- coding: utf-8

# File: start_demo.py
# Author: Thomas Wood: thomas.wood@huawei.com

import os
import time
import subprocess

def spin_demo_page():
    demo_command = "FLASK_APP=frontend.py flask run"
    p = subprocess.Popen(demo_command, shell=True)


if __name__ == "__main__":
    spin_demo_page()
