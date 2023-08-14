import argparse

from config import config
from jenkins.api import JenkinsApi
from win10toast import ToastNotifier


def deploy(target_alias):
    # read config
    server, deploy_list = config.read()
    target = next((item for item in deploy_list if item.alias == target_alias), None)
    if target is None:
        raise Exception(f'no such alias: {target_alias}')
    print('find deploy info: folder={}, job={}, branch={}'.format(target.folder, target.job, target.branch))
    # deploy
    toaster = ToastNotifier()

    jenkins = JenkinsApi(server.url, target.folder, server.username, server.token)
    build = jenkins.get_job_by_name(target.job).build_with_params({'BRANCH': target.branch})
    print('building build number: {}'.format(build.number))
    toaster.show_toast('Deploying\n job:{}\n branch:{}'.format(target.job, target.branch))
    build = build.refresh_until_finished()
    print('build result: {}'.format(build.result))
    toaster.show_toast('Deploy Success\n job:{}\n branch:{}'.format(target.job, target.branch))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Jenkins deploy script")

    parser.add_argument('-d', '--deploy', type=str, help='deploy')

    # config file
    sub_config_parser = parser.add_subparsers(title='config file', dest='config')
    config_parser = sub_config_parser.add_parser('config', help='config file')
    config_parser.add_argument('-g', '--generate', action='store_true', help='generate config file',
                               dest='generate_config_file')

    # parse args
    args = vars(parser.parse_args())

    # generate config file
    # if args.generate_config_file:
    if args.get('generate_config_file',None):
        config.generate_config_file()
        exit()

    if args.get('deploy', None) is not None:
        deploy(args.get('deploy'))
        exit()
