import yaml
from twisted.python import log


def read_blacklist(blacklistfile):
    blacklist = []
    dns_servers = []
    if not blacklistfile:
        log.err("No blacklist config file provided.")
    else:
        with open(str(blacklistfile), 'r') as blstream:
            bufferlist = yaml.load(blstream)
            blacklist = bufferlist.get('proxy-blacklist')
            dns_servers = bufferlist.get('dns-servers')
    return blacklist, dns_servers


def set_servers(dns_servers):
    cnt = 0
    for server in dns_servers:
        dns_servers[cnt] = dns_servers[cnt].strip("\"")
        cnt += 1
    return dns_servers
