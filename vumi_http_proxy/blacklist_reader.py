import yaml
import sys
from twisted.python import log


class FileReader(object):
    def __init__(self, blacklistfile):
        self.blacklist = []
        self.read_file(blacklistfile)

    def read_file(self, blacklistfile):
        if not blacklistfile:
            log.err("No blacklist config file provided.")
            self.safely_exit()
        else:
            with open(str(blacklistfile), 'r') as blstream:
                bufferlist = yaml.load(blstream)
                self.blacklist = bufferlist.get('proxy-blacklist')
        return self.blacklist

    def safely_exit(self):
        log.err("Ending process..")
        sys.exit()
