# aiohttpdemo_polls/settings.py
import pathlib
import argparse
import yaml
from trafaret_config import commandline
from utils import TRAFARET
# BASE_DIR = pathlib.Path(__file__).parent.parent
# config_path = BASE_DIR / 'config' / 'polls.yaml'

# def get_config(path):
#     with open(path) as f:
#         config = yaml.safe_load(f)
#     return config

# config = get_config(config_path)

BASE_DIR = pathlib.Path(__file__).parent.parent
DEFAULT_CONFIG_PATH = BASE_DIR / 'config' / 'polls.yaml'


def get_config(argv=None):
    ap = argparse.ArgumentParser()
    commandline.standard_argparse_options(
        ap,
        default_config=DEFAULT_CONFIG_PATH
    )

    # ignore unknown options
    options, unknown = ap.parse_known_args(argv)

    config = commandline.config_from_options(options, TRAFARET)
    return config

if __name__ == '__main__':
    get_config()