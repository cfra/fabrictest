#!/usr/bin/env python3

import time
import sys
import subprocess
import os

from topology import configs

from config import config_dir, state_dir, sbin_dir, user

ns = sys.argv[1]
config = configs[ns]

ns_config_dir = os.path.join(config_dir, ns)
ns_state_dir = os.path.join(state_dir, ns)


for interface in ['lo'] + config['links']:
    subprocess.check_call(['ip', 'link', 'set', interface, 'up'])

for directory in ns_config_dir, ns_state_dir:
    subprocess.check_call(['rm', '-rf', directory])
    subprocess.check_call(['mkdir', '-p', directory])
    subprocess.check_call(['chown', '%s:' % user, directory])

for daemon in config['daemons']:
    ns_config_file_path = os.path.join(ns_config_dir, '%s.conf' % daemon)
    with open(ns_config_file_path, 'w') as config_file:
        config_file.write(config['configfiles'][daemon])
    subprocess.check_call(['chown', '%s:' % user, ns_config_file_path])

children = []
for daemon in config['daemons']:
    children.append(subprocess.Popen([os.path.join(sbin_dir, daemon),
                                      '-A', '::1',
                                      '-N', ns,
                                      '-z', os.path.join(ns_state_dir, 'zserv.api'),
                                      '-u', 'root']))

while True:
    time.sleep(30)
