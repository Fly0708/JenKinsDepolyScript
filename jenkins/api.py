import requests
from requests import Response
from requests.auth import HTTPBasicAuth
from urllib.parse import urlparse, urlunparse


class JenkinsApi:
    def __init__(self, base_url, folder, username, api_token):
        self.base_url: str = base_url
        self.folder: str = folder
        self.url: str = base_url.rstrip('/') + '/' + folder
        self.username: str = username
        self.api_token: str = api_token

        self.auth = HTTPBasicAuth(username, api_token)
        self.jobs: list = self.job_list()
        self.job_dict: dict = {job.name: job for job in self.jobs}

    def send_http_request(self, url, url_params=None) -> Response:
        if url_params is None:
            url_params = {}
        origin = urlparse(self.url)
        result = urlparse(url)
        new_url = urlunparse((result.scheme, origin.netloc, result.path, result.params, result.query, result.fragment))
        return requests.get(new_url, auth=self.auth, params=url_params)

    def send_post_request(self, url, url_params=None) -> Response:
        if url_params is None:
            url_params = {}
        origin = urlparse(self.url)
        result = urlparse(url)
        new_url = urlunparse((result.scheme, origin.netloc, result.path, result.params, result.query, result.fragment))
        return requests.post(new_url, auth=self.auth, params=url_params)

    def job_list(self) -> list:
        response = self.send_http_request(self.url + '/api/json').json()
        jobs = response.get('jobs')
        if jobs is None:
            return []

        from jenkins.job import Job
        return [Job(self, job.get('name'), job.get('url')) for job in jobs]

    def get_job_dict(self):
        return self.job_dict

    def get_job_by_name(self, name):
        job = self.job_dict.get(name)
        if job is None:
            raise Exception("job not found")
        return job