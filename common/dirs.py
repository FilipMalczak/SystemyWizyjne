import os
from common import config

BASE_DIR_FOR_CONFIG = os.path.expanduser("~") # it is expected to be multiplatform http://stackoverflow.com/questions/4028904/how-to-get-the-home-directory-in-python
CONFIG_DIR = os.path.join(BASE_DIR_FOR_CONFIG, config.app_code)

def config(*names):
    os.path.join(CONFIG_DIR, *names)
