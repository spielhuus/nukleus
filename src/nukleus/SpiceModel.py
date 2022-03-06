import glob
import os
import re
from typing import List

#from .model import POS_T, GlobalLabel, LocalLabel, Pin, Symbol, Wire
#from .Schema import Schema


class spice_model:
    def __init__(self, keys, path, includes, content):
        self.keys = keys
        self.path = path
        self.includes = includes
        self.content = content


def __load_model__(filename: str):
    with open(filename) as file:
        content = file.read()
        keys = []
        includes = []
        for m in re.findall(r"\.SUBCKT ([a-zA-Z0-9]*) .*", content, re.IGNORECASE):
            keys.append(m)
        for m in re.findall(r"\.include (.*)", content, re.IGNORECASE):
            includes.append(m)

        return(spice_model(keys, filename, includes, content))


def load_spice_models(paths: List[str]) -> List[spice_model]:
    for path in paths:
        models = []
        for filename in glob.iglob(f'{path}/**', recursive=True):
            if filename in (".", ".."):
                continue
            if os.path.splitext(filename)[-1].lower() in (".lib", ".mod"):
                models.append(__load_model__(filename))

    return models


def __model_by_path__(path, models):
    for m in models:
        filename = m.path.split("/")[-1]
        if path == filename:
            return m

    return None


def __contains__(path, includes):
    for i in includes:
        if i.path == path:
            return True
    return False


def __get_includes__(path, includes, models):
    if not __contains__(path, includes):
        model = __model_by_path__(path, models)
        includes.append(model)
        for i in model.includes:
            __get_includes__(i)


def get_includes(key, includes, models):
    found = False
    for m in models:
        if key in m.keys:
            found = True
            if not __contains__(m.path, includes):
                includes.append(m)
                for i in m.includes:
                    __get_includes__(i, includes, models)

    assert found, f"Model not found {key}"
