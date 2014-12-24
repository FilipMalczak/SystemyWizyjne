import os

app_code="SW14"

# BASE_DIR_FOR_CONFIG = os.path.expanduser("~") # it is expected to be multiplatform http://stackoverflow.com/questions/4028904/how-to-get-the-home-directory-in-python
BASE_DIR_FOR_CONFIG = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CONFIG_DIR = os.path.join(BASE_DIR_FOR_CONFIG, app_code)

def config(*names):
    return os.path.join(CONFIG_DIR, *names)

vision_config = config("vision.json")

actions_config = config("default.actions")

recognition_dir = config("recognition")
models_dir = config("recognition", "models")
prob_boundaries = config("recognition", "probs.json")
hmm_state = config("recognition", "hmm_state.json")

def model(name):
    return config("recognition", "models", name)

NEEDED_DIRS = [
    CONFIG_DIR,
    recognition_dir,
    models_dir
]

for d in NEEDED_DIRS:
    if not os.path.exists(d):
        os.makedirs(d)
