from urllib.parse import urlparse


def normalizating_url(url):
    url_parse = urlparse(url)
    scheme = url_parse.scheme
    hostname = url_parse.netloc
    return f"{scheme.lower()}://{hostname.lower()}"