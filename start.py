#!/usr/bin/env python3

import subprocess
import os
import time
import random

from topology import namespaces, links

print("Creating namespaces")
for ns in namespaces:
    subprocess.call(['ip', 'netns', 'del', ns])
    subprocess.check_call(['ip', 'netns', 'add', ns])

print("Creating links")
for link in links:
    subprocess.check_call(['ip', 'link', 'add', link[0], 'netns', link[1],
                           'type', 'veth', 'peer', 'name', link[1], 'netns', link[0]])

base_dir = os.path.abspath(os.path.dirname(__file__))

def startup_delay():
    return random.uniform(0, len(namespaces) / 5)

print("Starting children")
children = []
for ns in namespaces:
    children.append(subprocess.Popen(['ip', 'netns', 'exec', ns,
                                      os.path.join(base_dir, 'netns_startup.py'), ns]))
    time.sleep(1)

print("Done")
while True:
    time.sleep(30)
