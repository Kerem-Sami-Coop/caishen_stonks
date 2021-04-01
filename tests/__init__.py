import sys
from pathlib import Path
import os

# Pytest has trouble identifying some imports without updating the
# python Path to include the app and tests modules
service_root = Path(__file__).parents[1]
sys.path.insert(0, f"{service_root}")
sys.path.insert(0, f"{service_root}/src")
sys.path.insert(0, f"{service_root}/tests")

if os.path.exists("secrets.yaml"):
    import yaml
    with open("secrets.yaml", "r") as f:
        yaml_config = yaml.safe_load(f)

    for key in yaml_config.keys():
        os.environ[key] = yaml_config[key]
