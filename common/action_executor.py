import os
from common.dirs import config

class ActionExecutor:

    # it should load action definitions from file

    def __init__(self, path=None):
        self.path = path if path else config("default.actions")
        self.definitions = {}


    def load(self):
        if os.path.exists(self.path):
            with open(self.path, 'r') as f:
                for line in f:
                    splat = line.split(';')
                    self.definitions[splat[0]] = splat[1]


    def execute(self, name):
        '''
        Executes action set to given gesture name.
        If there is no action for this name, print the name on stdout
        '''
        if name in self.definitions:
            print self.definitions[name]
        else:
            print name
