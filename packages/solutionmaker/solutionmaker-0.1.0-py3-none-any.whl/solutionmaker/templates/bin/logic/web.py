import requests
from bin.settings.settings import logger

def send_request(url_str, headers_dc=None, params_dc=None, cookies_dc=None, json_dc=None, method="GET") -> requests.Response:
    """
    Universal function to complete requests

    method: "GET" | "POST" | "PUT" | "DELETE" | "PATCH"
    """
    try:
        response = requests.request(
            method=method,
            url=url_str,
            headers=headers_dc,
            params=params_dc,
            cookies=cookies_dc,
            json=json_dc
        )
        response.raise_for_status()
    except requests.RequestException as e:
        logger.info(f"ER - request error: {e}")
        response = None

    return response


def get_html_response_from_url(url_str, headers_dc, params_dc=None, cookies_dc=None, json_dc=None, request_type_str="GET") -> (str, int):
    response = send_request(url_str, headers_dc, params_dc, cookies_dc, json_dc, request_type_str)
    return (response.text, response.status_code) if response else ("", 500)


def get_json_response_from_url(url_str, headers_dc, params_dc=None, cookies_dc=None, json_dc=None, request_type_str="GET") -> (dict, int):
    response = send_request(url_str, headers_dc, params_dc, cookies_dc, json_dc, request_type_str)
    if response:
        try:
            return response.json(), response.status_code
        except ValueError:
            logger.info("ER - impossible to decode json.")
            return {}, 500
    return {}, 500