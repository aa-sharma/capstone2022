import json
import os
from os.path import dirname, join, abspath
from datetime import datetime

ROOT_DIR = dirname(abspath(join(__file__, "..")))


def read_json(file_path):
    with open(join(ROOT_DIR, file_path), "r") as f:
        data = json.load(f)
        return data


def create_folder_file_now(directory=None, file_name=None, file_type='log'):
    """Creates a folder and file path in the form /'directory'/month/day/'file_name'.'file_type'
    :param directory: The directory you wish to stores the folder file path
    :param file_name: The file name
    :param file_type: The file extension eg. 'log', 'png' etc.
    :returns: the full path to the file """
    if directory is None or file_name is None:
        raise FileNotFoundError('Directory or filename was not specified')
    else:
        now = datetime.now()
        os.system(f'mkdir -p {os.path.join(ROOT_DIR, directory, now.strftime("%B"), now.strftime("%d"))}')
        file = os.path.join(ROOT_DIR, directory, now.strftime("%B"), now.strftime("%d"),
                            f'{file_name}_{now.strftime("%H")}-{now.strftime("%M")}.{file_type}')

        return file
