import yaml
import sys
from twisted.python import log


def read_blacklist(blacklistfile):
    blacklist = []
    if not blacklistfile:
        log.err("No blacklist config file provided.")
    else:
        with open(str(blacklistfile), 'r') as blstream:
            bufferlist = yaml.load(blstream)
            blacklist = bufferlist.get('proxy-blacklist')
    return blacklist


def safely_exit(self):
    log.err("Ending process..")
    sys.exit()
