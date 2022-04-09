import glob
import os
import re
from typing import List


class spice_model:
    def __init__(self, keys, path, includes, content):
        self.keys = keys
        self.path = path
        self.includes = includes
        self.content = content


def _load_model(filename: str) -> spice_model:
    with open(filename) as file:
        content = file.read()
        keys = []
        includes = []
        for model in re.findall(r"\.SUBCKT ([a-zA-Z0-9]*) .*", content, re.IGNORECASE):
            keys.append(model)
        for model in re.findall(r"\.model ([a-zA-Z0-9]*) .*", content, re.IGNORECASE):
            keys.append(model)
        for model in re.findall(r"\.include (.*)", content, re.IGNORECASE):
            includes.append(model)

        return spice_model(keys, filename, includes, content)


def load_spice_models(paths: List[str]) -> List[spice_model]:
    models = []
    for path in paths:
        for filename in glob.iglob(f'{path}/**', recursive=True):
            if filename in (".", ".."):
                continue
            if os.path.splitext(filename)[-1].lower() in (".lib", ".mod"):
                models.append(_load_model(filename))

    return models


def _model_by_path(path, models):
    for model in models:
        filename = model.path.split("/")[-1]
        if path == filename:
            return model
    return None


def _contains(path, includes):
    for i in includes:
        if i.path == path:
            return True
    return False


def _get_includes(path, includes, models):
    if not _contains(path, includes):
        model = _model_by_path(path, models)
        includes.append(model)
        for i in model.includes:
            _get_includes(i, includes, models)


def get_includes(key, includes, models):
    found = False
    for model in models:
        print(f'match model: {model}')
        if key in model.keys:
            found = True
            if not _contains(model.path, includes):
                includes.append(model)
                for i in model.includes:
                    _get_includes(i, includes, models)

    assert found, f"Model not found {key}"
