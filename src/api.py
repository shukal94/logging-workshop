import requests
from requests.adapters import HTTPAdapter, Retry


class HttpClient:

    def __init__(self, max_retries: int, retry_delay: float):
        self.retries = Retry(
            total=max_retries,
            backoff_factor=retry_delay,
            status_forcelist=[
                requests.codes.internal_server_error,
                requests.codes.bad_gateway,
                requests.codes.unavailable,
                requests.codes.gateway_timeout
            ]
        )

        self.session = requests.Session()
        self.session.mount("http://", HTTPAdapter(max_retries=self.retries))

    def get(self, url: str, params=None, headers=None, **kwargs):
        return self.session.get(url=url, params=params, headers=headers, **kwargs)

    def post(self, url: str, params=None, headers=None, data=None, json=None, **kwargs):
        return self.session.post(url=url, params=params, headers=headers, data=data, json=json, **kwargs)

    def put(self, url: str, params=None, headers=None, data=None, json=None, **kwargs):
        return self.session.put(url=url, params=params, headers=headers, data=data, json=json, **kwargs)

    def patch(self, url: str, params=None, headers=None, data=None, json=None, **kwargs):
        return self.session.patch(url=url, params=params, headers=headers, data=data, json=json, **kwargs)

    def delete(self, url: str, params=None, headers=None, data=None, json=None, **kwargs):
        return self.session.delete(url=url, params=params, headers=headers, data=data, json=json, **kwargs)


class BaseApi:
    http_client: HttpClient

    def __init__(self, http_client: HttpClient):
        self.http_client = http_client


class JsonPlaceholderApi(BaseApi):
    base_url: str
    POSTS = "posts"

    def __init__(self, http_client: HttpClient, base_url: str):
        super().__init__(http_client)
        self.base_url = base_url

    def get_posts(self):
        response = self.http_client.get(url=f"{self.base_url}/{self.POSTS}")
        response.raise_for_status()
        return response.json()
