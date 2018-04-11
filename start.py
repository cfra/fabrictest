#!/usr/bin/env python

import subprocess
import os
import time

from topology import namespaces, links

for ns in namespaces:
    subprocess.call(['ip', 'netns', 'del', ns])
    subprocess.check_call(['ip', 'netns', 'add', ns])

for link in links:
    subprocess.check_call(['ip', 'link', 'add', link[0], 'netns', link[1],
                           'type', 'veth', 'peer', 'name', link[1], 'netns', link[0]])

base_dir = os.path.abspath(os.path.dirname(__file__))

children = []
for ns in namespaces:
    children.append(subprocess.Popen(['ip', 'netns', 'exec', ns,
                                      os.path.join(base_dir, 'netns_startup.py'),
                                      ns]))

while True:
    time.sleep(30)
