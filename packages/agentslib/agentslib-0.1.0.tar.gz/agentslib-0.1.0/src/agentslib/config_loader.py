import yaml
import importlib.resources  # Python 3.9+

def load_prompts():
    with importlib.resources.files("agentslib.config").joinpath("prompts.yaml").open("r") as f:
        return yaml.safe_load(f)
