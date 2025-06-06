# Config.py
import importlib.util
import os
from collections import defaultdict

from act.facades.Constant.Constant import CONFIG_PATH


def merge_dicts(dict1, dict2):
    merged = dict1.copy()
    for key, value in dict2.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = merge_dicts(merged[key], value)
        else:
            merged[key] = value
    return merged

def load_configs_from_directory(directory):
    merged_config = defaultdict(dict)
    for filename in os.listdir(directory):
        if filename.endswith('.py'):
            module_name = filename[:-3]
            module_path = os.path.join(directory, filename)
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, 'get_config'):
                configValue = module.get_config()
                merged_config.setdefault(module_name, configValue)
    return dict(merged_config)

def Config(key:str, default = None):
    keyList = key.split(".")

    temp = default

    obj = load_configs_from_directory(CONFIG_PATH)

    for i in keyList:
        if i in obj :
            obj = obj.get(i)
            temp = obj

    return  temp


if __name__ == "__main__":
    # print(Config("app.emulatorPath"))
    print(Config("app.itemCollectionTopLever.switch"))