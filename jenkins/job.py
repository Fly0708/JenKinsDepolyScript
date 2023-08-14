from jenkins.api import JenkinsApi
from jenkins.build import Build
import time


class Job:
    def __init__(self, _jenkins_api: JenkinsApi, name, url):
        self._jenkins_api = _jenkins_api
        self.name = name
        self.url = url.rstrip('/')

    def last_build(self) -> Build:
        response = self._jenkins_api.send_http_request(self.url + '/api/json').json()
        last_build = response.get('lastBuild')
        if last_build is None:
            return None
        last_build = self._jenkins_api.send_http_request(last_build.get('url') + '/api/json').json()
        return Build(self._jenkins_api, last_build.get('number'), last_build.get('url'), last_build.get('timestamp'),
                     last_build.get('result'), last_build.get('building'))

    def build_with_params(self, params: dict) -> Build:
        last = self.last_build().number
        self._jenkins_api.send_post_request(self.url + '/buildWithParameters', params)
        while True:
            build = self.last_build()
            if build.number != last:
                return build
            time.sleep(1)
