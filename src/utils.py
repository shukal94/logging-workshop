import os
import re
import logging
import configparser
import json
from typing import Any

import requests

# let's supress utils logger, we always can change level to DEBUG in config
LOGGER = logging.getLogger("utils")


def load_config(path: str):
    LOGGER.debug(f"Reading global project config from {path}")
    config = configparser.ConfigParser()
    config.read(path)
    return config


def env(key: str, safe=True):
    value = os.getenv(key)
    if not safe and not value:
        raise KeyError(f"{key} was not found!")
    return value


def read_from_file(path: str):
    LOGGER.debug(f"Reading from {path}.")
    with open(path, 'r') as file:
        content = file.read()
    return content


def write_to_file(content: str, path: str):
    LOGGER.debug(f"Writing to {path}.")
    with open(path, 'w') as file:
        file.write(content)


class SensitiveInfoFilter(logging.Filter):
    patterns = [r":\/\/(.*?)\@"]
    sensitive_keys = (
        "headers",
        "credentials",
        "Authorization",
        "token",
        "password",
    )

    def filter(self, record):
        try:
            record.args = self.mask_sensitive_args(record.args)
            record.msg = self.mask_sensitive_msg(record.msg)
            return True
        except Exception as e:
            return True

    def mask_sensitive_args(self, args):
        if isinstance(args, dict):
            new_args = args.copy()
            for key in args.keys():
                if key in self.sensitive_keys:
                    new_args[key] = "******"
                else:
                    # mask sensitive data in dict values
                    new_args[key] = self.mask_sensitive_msg(args[key])
            return new_args
        # when there are multi arg in record.args
        return tuple([self.mask_sensitive_msg(arg) for arg in args])

    def mask_sensitive_msg(self, message):
        # mask sensitive data in multi record.args
        if isinstance(message, dict):
            return self.mask_sensitive_args(message)
        if isinstance(message, str):
            for pattern in self.patterns:
                message = re.sub(pattern, "//:******@", message)
            for key in self.sensitive_keys:
                pattern_str = rf"'{key}': '[^']+'"
                replace = f"'{key}': '******'"
                message = re.sub(pattern_str, replace, message)
        return message


def request_response_log_interceptor(response: requests.Response, *args, **kwargs):
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


def log_query(statement: str):
    LOGGER.info(f"Executing SQL Query: {statement}")


def log_query_output(output: list | Any):
    to_log = ""
    if isinstance(output, list):
        for output_entry in output:
            output_entry = str(output_entry)
            to_log = to_log + output_entry + "\n"
    else:
        to_log = to_log.join(str(output))
    LOGGER.info(f"SQL Query result:\n{to_log}")
