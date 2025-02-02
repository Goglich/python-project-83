from urllib.parse import urlparse
import urllib
import requests
from bs4 import BeautifulSoup


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
    except requests.exceptions.RequestException:
        return None


def get_markup(url):
    return urllib.request.urlopen(url)


def html_parse(url):
    markup = get_markup(url)
    soup = BeautifulSoup(markup)
    if soup.find("h1"):
        h1 = soup.find("h1").text
    else:
        h1 = None
    title = soup.title.string
    description = soup.find(
        'meta',
        attrs={'name': 'description'}).get('content')
    tags = {
        'h1': h1,
        'title': title,
        'description': description
    }
    return tags
