import ipaddress
import jinja2
import os

from config import topo_width as width
from config import topo_height as height

namespaces = []
for x in range(width):
    for y in range(height):
        namespaces.append('rt-%d-%d' % (x,y))

links = []
for y in range(height - 1):
    for x in range(width):
        for x2 in range(width):
            links.append(('rt-%d-%d' % (x,y),
                               'rt-%d-%d' % (x2,y+1)))

templatedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config_templates')

configs = {}

def config_for(ns, daemon):
    templatefile_path = os.path.join(templatedir, '%s.j2' % daemon)
    with open(templatefile_path, 'r') as templatefile:
        template = jinja2.Template(templatefile.read())

    context = {
            'ns': ns,
            'daemon': daemon
    }
    context.update(configs[ns])
    return template.render(context)

for idx,ns in enumerate(namespaces):
    configs[ns] = {
            'loopback_v4': ipaddress.IPv4Address('100.0.0.1') + idx,
            'loopback_v6': ipaddress.IPv6Address('2001:db8:64::1') + idx,
            'net': '49.0000.0000.%04x.00' % (idx + 1),
            'links': sorted([ link[1] for link in links if link[0] == ns ]
                          + [ link[0] for link in links if link[1] == ns ]),
            'daemons': ['zebra', 'fabricd'],
            'configfiles': {},
    }
    for daemon in configs[ns]['daemons']:
        configs[ns]['configfiles'][daemon] = config_for(ns, daemon)
