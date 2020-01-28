import logging
import argparse
import os
import subprocess
import yaml

WORKSPACE = f'{os.getenv("HOME")}/.memo/'
CONFIG_FILE = WORKSPACE + '.config'
STATE_FILE = WORKSPACE + '.state'
LOG_FILE = WORKSPACE + '.log'
EDITORS = [
    'vim',
    'nano',
]


def parse_options():
    """ parse command line options """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--config',
        dest='show_config',
        help='show_config',
        default=False,
        action='store_true',
    )
    parser.add_argument(
        '-n',
        '--new',
        dest='new_name',
        help='create new memo',
        default=False,
        action='store',
    )
    parser.add_argument(
        '-l',
        '--list',
        dest='list',
        help='list all memos',
        default=False,
        action='store_true',
    )
    return parser.parse_args()


def list_memos(*, offset=0, limit=15):
    for f in os.listdir(WORKSPACE):
        if not f.startswith('.'):
            print(f)


class Memo:
    def __init__(self):
        if not os.path.exists(WORKSPACE):
            os.mkdir(WORKSPACE)
            with open(CONFIG_FILE, 'w'):
                pass
            with open(STATE_FILE, 'w'):
                pass
            with open(LOG_FILE, 'w'):
                pass
        if 'editor' not in self.config:
            self.__setup_editor()

    def __setup_editor(self):
        for e in EDITORS:
            found = not subprocess.call(['which', e])
            if found:
                self.__update_config('editor', e)
                break

    def __update_config(self, key, value):
        with open(CONFIG_FILE, 'w') as f:
            f.write(yaml.safe_dump(dict([*self.config.items(), (key, value)])))

    @property
    def config(self):
        with open(CONFIG_FILE) as f:
            try:
                return yaml.safe_load(f.read()) or {}
            except yaml.scanner.ScannerError:
                raise RuntimeError('config file is corrupted')


def main():
    logging.basicConfig(
        level=logging.ERROR, format='%(asctime)s %(levelname)s: %(message)s')
    options = parse_options()
    memo = Memo()
    if options.list:
        list_memos()
    elif options.new_name:
        # if exists, open or create new with suffix?
        new_file_path = WORKSPACE + options.new_name
        with open(new_file_path, 'w'):
            pass
        subprocess.call([memo.config['editor'], new_file_path])
    elif options.show_config:
        with open(CONFIG_FILE) as f:
            for l in f.readlines():
                print(l)


if __name__ == '__main__':
    main()