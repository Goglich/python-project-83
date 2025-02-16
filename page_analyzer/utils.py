from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup


def normalize_url(url):
    url_parse = urlparse(url)
    scheme = url_parse.scheme
    hostname = url_parse.netloc
    return f"{scheme.lower()}://{hostname.lower()}"


def get_page_data(url):
    try:
        response = requests.get(url['name'])
        markup = response.text
        soup = BeautifulSoup(markup)
        if soup.find("h1"):
            h1 = soup.find("h1").text
        else:
            h1 = None
        title = soup.title.string
        try:
            description = soup.find(
                'meta',
                attrs={'name': 'description'}).get('content')
        except requests.exceptions:
            description = ''
        tags = {
            'h1': h1,
            'title': title,
            'description': description
        }
        response.raise_for_status()
        return response.status_code, tags
    except requests.exceptions.RequestException:
        return None, None
