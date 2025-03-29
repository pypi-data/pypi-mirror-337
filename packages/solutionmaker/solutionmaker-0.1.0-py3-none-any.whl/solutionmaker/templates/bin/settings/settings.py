# solutionmaker/templates/bin/settings/settings.py
import os
import logging
import json
import datetime

# Calculation root directory of the project
CURRENT_FILE = os.path.abspath(__file__)  # Path to this settings.py
SETTINGS_DIR = os.path.dirname(CURRENT_FILE)  # bin/settings
BIN_DIR = os.path.dirname(SETTINGS_DIR)  # bin
BASE_DIR = os.path.dirname(BIN_DIR)  # Root directory

PROJECT_TITLE = os.path.basename(BASE_DIR)# title of project root folder is a title of the project

TIMESTAMP_CURRENT_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

# Basic directories
RESULTS_DIR = os.path.join(BASE_DIR, "results")
SOURCE_DIR = os.path.join(BASE_DIR, "source")

# Creation directories
for directory in [RESULTS_DIR, SOURCE_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Files for storing config and cookies
CONFIG_FILE = os.path.join(SETTINGS_DIR, "config.json")
COOKIES_FILE = os.path.join(SETTINGS_DIR, "cookies.json")

# Logger settings
LOG_FILE = os.path.join(BASE_DIR, "logs.txt")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, mode='a', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# Functions for handling configuration
def load_config_fc():
    #default_config = {"id": "11", "value": "anything"}
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_config_fc(config_dc):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config_dc, f)

# Functions for handling cookies
def load_cookies_fc():
    if os.path.exists(COOKIES_FILE):
        with open(COOKIES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_cookies_fc(cookies_dc):
    with open(COOKIES_FILE, 'w', encoding='utf-8') as f:
        json.dump(cookies_dc, f)

def get_timestamp_current_str_fc():
    return TIMESTAMP_CURRENT_str
