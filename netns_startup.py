#!/usr/bin/env python

import time
import sys
import subprocess
import os

from topology import configs
from config import config_dir, state_dir, user

ns = sys.argv[1]
config = configs[ns]

ns_config_dir = os.path.join(config_dir, ns)
ns_state_dir = os.path.join(state_dir, ns)

subprocess.check_call(['ip', 'link', 'set', 'lo', 'up'])
for directory in ns_config_dir, ns_state_dir:
    subprocess.check_call(['rm', '-rf', directory])
    subprocess.check_call(['mkdir', '-p', directory])
    subprocess.check_call(['chown', '%s:' % user, directory])

while True:
    time.sleep(30)
