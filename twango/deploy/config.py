import sys
import pprint 

class Config:

    def _loadfile(self, name):
        __import__(name)
        return sys.modules[name]

    def pprint(self):   
        pp = pprint.PrettyPrinter(indent=4)
        for setting in dir(self):
            if setting == setting.upper():
                attr = getattr(self, setting)
                print setting
                pp.pprint(attr)

    def load(self, config=None, hosts=None):
        try:
            c = config if config else 'settings'
            mod = self._loadfile(c)
        except ImportError, e:
            raise ImportError("Could not import settings '%s': %s" % (c, e))

        for setting in dir(mod):
            if setting == setting.upper():
                setattr(self, setting, getattr(mod, setting))

        try:
            mod = self._loadfile(hosts if hosts else 'nodes')
            self.NODES = getattr(mod, 'NODES')
        except ImportError, e:
            self.NODES = {}

settings = Config()
settings.load()

