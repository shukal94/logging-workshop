import json
import requests
import logging
from requests.adapters import HTTPAdapter, Retry


LOGGER = logging.getLogger("api")


def api_interceptor(response: requests.Response, *args, **kwargs):
    request: requests.PreparedRequest = response.request
    log_request(request)
    log_response(response)


def log_request(request: requests.PreparedRequest):
    request_headers = headers_to_str(request.headers)
    request_body = body_to_str(request.body)
    request_log = "# ========== REQUEST ========== #\n" + \
                  f"{request.method} {request.url}\n" + \
                  f"{request_headers}\n" + \
                  f"{request_body}"
    LOGGER.info(request_log)


def log_response(response: requests.Response):
    response_headers = headers_to_str(response.headers)
    response_body = body_to_str(response.content)
    response_log = "# ========== RESPONSE ========== #\n" + \
                   f"HTTP{response.status_code}\n" + \
                   f"{response_headers}\n" + \
                   f"{response_body}"
    LOGGER.info(response_log)


def headers_to_str(headers):
    return "\n".join(f"'{key}': '{value}'" for key, value in headers.items())


# what if body not JSON??? TODO: add content-type dependency
def body_to_str(body):
    return "" if not body else json.dumps(json.loads(body.decode("utf-8")), indent=2)


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
        # Yet another approach: add an event listener. The only one event listener available in requests: 'response'
        self.session.hooks['response'].append(api_interceptor)
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

    def get_posts(self, user_id=None):
        params = {"userId": user_id}
        response = self.http_client.get(url=f"{self.base_url}/{self.POSTS}", params=params)
        response.raise_for_status()
        return response.json()

    def get_post_by_id(self, post_id: int):
        response = self.http_client.get(url=f"{self.base_url}/{self.POSTS}/{post_id}")
        response.raise_for_status()
        return response.json()

    def create_post(self, payload: dict):
        headers = {"Content-type": "application/json; charset=UTF-8"}
        response = self.http_client.post(
            url=f"{self.base_url}/{self.POSTS}",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()

    def update_post(self, post_id: int, payload: dict):
        headers = {"Content-type": "application/json; charset=UTF-8"}
        response = self.http_client.put(
            url=f"{self.base_url}/{self.POSTS}/{post_id}",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()

    def patch_post(self, post_id: int, payload: dict):
        headers = {"Content-type": "application/json; charset=UTF-8"}
        response = self.http_client.patch(
            url=f"{self.base_url}/{self.POSTS}/{post_id}",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()

    def delete_post(self, post_id: int):
        response = self.http_client.delete(url=f"{self.base_url}/{self.POSTS}/{post_id}")
        response.raise_for_status()
        return response.json()
