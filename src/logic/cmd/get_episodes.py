import sys
import re
import urllib.request

from bs4 import BeautifulSoup
from src.custom_logging import setup_logger
from src.logic.cmd.constants import url, parse_cli_arguments

logger = setup_logger(__name__)

seasonArg = parse_cli_arguments('1', 3)

return_array = []

def get_episodes(url_path, season):
    url = "{}staffel-{}/".format(url_path, season)
    html_page = urllib.request.urlopen(url, timeout=50)
    soup = BeautifulSoup(html_page, features="html.parser")
    pattern = re.compile(r"/.*/staffel-(?P<seasonNr>\d+)/episode-(?P<episodeNr>\d+)")
    for link in soup.findAll('a'):
        href = str(link.get("href"))
        search = pattern.search(href, re.M)
        if search is None:
            continue
        seasonNr = search.group('seasonNr')
        episodeNr = search.group('episodeNr')
        if seasonNr == season:
            if episodeNr not in return_array:
                return_array.append(episodeNr)
    return return_array

print(get_episodes(url, seasonArg))