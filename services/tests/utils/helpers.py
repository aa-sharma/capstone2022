import json
from os.path import dirname, join, abspath

ROOT_DIR = dirname(abspath(join(__file__, "..")))


def read_json(file_path):
    with open(join(ROOT_DIR, file_path), "r") as f:
        data = json.load(f)
        return data
