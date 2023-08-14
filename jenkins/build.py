import time

from jenkins.api import JenkinsApi


class Build:
    def __init__(self, _jenkins_api: JenkinsApi, number: int, url: str, timestamp: int = None, result: str = None,
                 building: bool = None, change: str = None):
        self._jenkins_api = _jenkins_api
        self.number = number
        self.url = url
        self.timestamp = timestamp
        self.result = result
        self.is_success = (result == 'SUCCESS')
        self.building = building
        self.change = change
        self.change_show_flag = True

    def refresh(self):
        response = self._jenkins_api.send_http_request(self.url + '/api/json').json()
        self.timestamp = response.get('timestamp')
        self.result = response.get('result')
        self.building = response.get('building')
        self.is_success = (self.result == 'SUCCESS')
        changeSet = response.get('changeSet')
        if changeSet is not None:
            self.change = [change.get('msg') for change in changeSet.get('items')]
            if self.change_show_flag:
                print('修改内容：\n')
                print('\n'.join(self.change))

    def refresh_until_finished(self, interval=5):
        while self.building:
            self.refresh()
            time.sleep(interval)
        return self
