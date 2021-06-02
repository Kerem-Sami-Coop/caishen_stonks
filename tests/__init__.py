import sys
from pathlib import Path
import os
import yaml


# Pytest has trouble identifying some imports without updating the
# python Path to include the app and tests modules
service_root = Path(__file__).parents[1]
sys.path.insert(0, f"{service_root}")
sys.path.insert(0, f"{service_root}/tests")

with open("dev_env_var.yaml", "r") as f:
    yaml_config = yaml.safe_load(f)

if os.path.exists("secrets.yaml"):
    with open("secrets.yaml", "r") as f:
        yaml_config.update(yaml.safe_load(f))

for key in yaml_config.keys():
    os.environ[key] = yaml_config[key]
