import os
from common import dirs

class ActionExecutor:

    # it should load action definitions from file

    def __init__(self, path=None):
        self.path = path if path else dirs.actions_config
        self.definitions = {}
        self.load()


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
            print self.definitions[name]    #TODO: make it do stuff
        else:
            print name
