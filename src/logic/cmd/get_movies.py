import sys
import re
import urllib.request

from bs4 import BeautifulSoup
from src.custom_logging import setup_logger
from src.logic.cmd.constants import url

logger = setup_logger(__name__)

return_array = []

def get_movies(url_path):
    url = "{}filme/".format(url_path)
    html_page = urllib.request.urlopen(url, timeout=50)
    soup = BeautifulSoup(html_page, features="html.parser")
    pattern = re.compile(r"/.*/film-(?P<filmNr>\d+)")
    for link in soup.findAll('a'):
        href = str(link.get("href"))
        search = pattern.search(href, re.M)
        if search is None:
            continue
        filmNr = search.group('filmNr')
        if filmNr not in return_array:
            return_array.append(filmNr)
    return return_array

print(get_movies(url))