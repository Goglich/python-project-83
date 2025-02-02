from urllib.parse import urlparse
import requests


def normalizating_url(url):
    url_parse = urlparse(url)
    scheme = url_parse.scheme
    hostname = url_parse.netloc
    return f"{scheme.lower()}://{hostname.lower()}"


def get_status_code(url):
    try:
        response = requests.get(url['name'])
        response.raise_for_status()
        return response.status_code
    except:
        return None
    