import sys
import re
import urllib.request

from bs4 import BeautifulSoup
from src.custom_logging import setup_logger
from src.logic.cmd.constants import url

logger = setup_logger(__name__)

return_array = []

def get_seasons(url_path):
    html_page = urllib.request.urlopen(url_path, timeout=50)
    soup = BeautifulSoup(html_page, features="html.parser")
    pattern = re.compile(r"/.*/staffel-(?P<seasonNr>\d+)")
    for link in soup.findAll('a'):
        episode = str(link.get("href"))
        search = pattern.search(episode, re.M)
        if search is None:
            continue
        seasonNr = search.group('seasonNr')
        if seasonNr not in return_array:
            return_array.append(seasonNr)
    return return_array

print(get_seasons(url))