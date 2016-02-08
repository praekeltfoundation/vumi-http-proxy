"""Reader class for specified .yml configuration file
    proxy-blacklist: [list of ip addresses to blacklist]
    dns-servers: [list of manual dns servers to use]

.. moduleauthor:: Carla Wilby <thisiscarlawilby@gmail.com>

"""

import yaml
from twisted.python import log


def read_config(configfile):
    """
    Retrieve content from configuration file as blacklist and dns servers lists
    """
    blacklist = []
    dns_servers = []
    if not configfile:
        log.err("No PyYAML config file provided.")
    else:
        with open(str(configfile), 'r') as blstream:
            bufferlist = yaml.load(blstream)
            blacklist = bufferlist.get('proxy-blacklist')
            dns_servers = parse_servers(bufferlist.get('dns-servers'))
    return blacklist, dns_servers


def parse_servers(dns_servers):
    dns_servers = [tuple(server) for server in dns_servers]
    return dns_servers
