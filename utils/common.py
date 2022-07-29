import json
import logging
from enum import IntEnum

class STAGE(IntEnum):
    IDLE = 0
    ONGOING_TRANSFER = 1
    DONE = 2


class FILETYPE(IntEnum):
    DIRECTORY = 0
    FILE = 1


class PAGE(IntEnum):
    FORM_PAGE = 0
    MAIN_PAGE = 1


def load_from_json_file(file_path: str) -> dict:
    with open(file_path) as f:
        data = json.load(f)
    return data


def get_logger():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filemode='w', filename='ssh_interface.log', level=logging.INFO)
    return logging


LOGGER = get_logger()
