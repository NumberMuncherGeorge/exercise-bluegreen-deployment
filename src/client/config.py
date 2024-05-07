import os
import sys
import yaml
import argparse
import logging

# from google.cloud.logging_v2.handlers.structured_log import StructuredLogHandler
from typing import TypeAlias, get_type_hints, Union, Any

class AppConfigError(Exception):
    pass

# Logger Config
logger = logging.getLogger()

stream_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# gcp_log_handler = StructuredLogHandler()
# logger.addHandler(gcp_log_handler)

logger.setLevel(logging.INFO)

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument("endpoints_yaml", help="Path to yaml file describing the endpoints to poll for version", type=str)
parser.add_argument("--poll-interval", default=os.environ.get('POLL_INTERVAL', '5'), help="Interval in seconds between pulling for version data", type=str)
parser.add_argument("--output-file", default=os.environ.get("OUTPUT_FILE", "output.ndjson"), help="Path to output file where results are stored", type=str)
config = parser.parse_args()

logger.info("Config looks good")

# Memberships
with open(config.endpoints_yaml) as endpoints_yaml:
    try:
        config.endpoints = yaml.safe_load(endpoints_yaml)['endpoints']
    except yaml.YAMLError as err:
        logger.error("Unable to parse endpoints definition file")
        exit(err)

logger.info("Polling endpoints loaded into config")
