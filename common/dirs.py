import os

app_code="SW14"

# BASE_DIR_FOR_CONFIG = os.path.expanduser("~") # it is expected to be multiplatform http://stackoverflow.com/questions/4028904/how-to-get-the-home-directory-in-python
BASE_DIR_FOR_CONFIG = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CONFIG_DIR = os.path.join(BASE_DIR_FOR_CONFIG, app_code)

def config(*names):
    os.path.join(CONFIG_DIR, *names)
