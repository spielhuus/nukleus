import glob
import os
import re
import logging
from typing import List


class spice_model:
    """Spice Model"""
    def __init__(self, keys, path, includes, content):
        self.keys: List[str] = keys
        """the keys of the model"""
        self.path: str = path
        """the path of the model"""
        self.includes: List[str] = includes
        """the includes of the model"""
        self.content:str = content
        """the content of the model"""

def _load_model(filename: str) -> spice_model:
    with open(filename, 'r', encoding='utf-8') as file:
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
    """
    Load the spice models from the paths.

    :param paths List[str]: The path to the models.
    :rtype List[spice_model]: List of spice models.
    """
    models = []
    for path in paths:
        for filename in glob.iglob(f'{path}/**', recursive=True):
            if filename in (".", ".."):
                continue
            if os.path.splitext(filename)[-1].lower() in (".lib", ".mod"):
                models.append(_load_model(filename))

    return models

def _model_by_path(path: str, models: List[spice_model]) -> spice_model:
    for model in models:
        filename = model.path.split("/")[-1]
        if path == filename:
            return model
    raise Exception(f"Model not found {path}")


def _contains(path: str, includes: List[spice_model]) -> bool:
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


def get_includes(key: str, includes: List[spice_model], models: List[spice_model]):
    """
    Get the includes and write them to the includes list.

    :param key str: The model key.
    :param includes List[spice_model]: The target list.
    :param models List[spice_model]: Models to search in.
    """
    for model in models:
        if key in model.keys:
            if not _contains(model.path, includes):
                includes.append(model)
                for i in model.includes:
                    _get_includes(i, includes, models)

    logging.warning("Model not found %s", key)
