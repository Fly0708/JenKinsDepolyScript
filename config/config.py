# generate config file if not exist, else return
import os

import yaml

_CONFIG_FILE = 'config.yml'


def get_config_file_path():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), _CONFIG_FILE)


def generate_config_file():
    config_file_path = get_config_file_path()
    if os.path.exists(config_file_path):
        return
    empty_config_template = {'server': {'url': '', 'username': '', 'token': ''}}
    with open(config_file_path, 'w') as f:
        yaml.dump(empty_config_template, f)


class Server(object):
    def __init__(self, url: str, username: str, token: str):
        self.url = url
        self.username = username
        self.token = token

    @staticmethod
    def read_server_from_dict(server_dict: dict) -> 'Server':
        return Server(server_dict['url'], server_dict['username'], server_dict['token'])


class Deploy(object):

    def __init__(self, folder: str, job: str, branch: str, alias: str):
        self.folder = folder
        self.job = job
        self.branch = branch
        self.alias = alias

    @staticmethod
    def read_deploy_list_from_dict(deploy_dict: dict) -> list['Deploy']:
        result = []
        for folder, jobs, in deploy_dict.items():
            for job, branches in jobs.items():
                for branch, alias in branches.items():
                    result.append(Deploy(folder, job, branch, str(alias)))
        return result


def read():
    with open(get_config_file_path(), 'r') as file:
        data = yaml.safe_load(file)
        server = Server.read_server_from_dict(data.get('server'))
        deploy_list = Deploy.read_deploy_list_from_dict(data.get('deploy'))
        return server, deploy_list
