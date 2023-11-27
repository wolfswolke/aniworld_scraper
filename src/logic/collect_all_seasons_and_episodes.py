import logging
import urllib.request

from bs4 import BeautifulSoup

# ------------------------------------------------------- #
#                   definitions
# ------------------------------------------------------- #
MODULE_LOGGER_HEAD = "collect_all_seasons_and_episodes.py -> "

# ------------------------------------------------------- #
#                   global variables
# ------------------------------------------------------- #

# ------------------------------------------------------- #
#                      functions
# ------------------------------------------------------- #


def get_season(url_path):
    logging.debug(MODULE_LOGGER_HEAD + "Entered get_season.")
    logging.debug(MODULE_LOGGER_HEAD + "Site URL is: " + url_path)
    counter_seasons = 1
    html_page = urllib.request.urlopen(url_path, timeout=50)
    soup = BeautifulSoup(html_page, features="html.parser")
    for link in soup.findAll('a'):
        seasons = str(link.get("href"))
        if "/staffel-{}".format(counter_seasons) in seasons:
            counter_seasons = counter_seasons + 1
    logging.debug(MODULE_LOGGER_HEAD + "Now leaving Function get_season")
    return counter_seasons - 1


def get_episodes(url_path, season_count):
    logging.debug(MODULE_LOGGER_HEAD + "Entered get_episodes")
    url = "{}staffel-{}/".format(url_path, season_count)
    episode_count = 1
    html_page = urllib.request.urlopen(url, timeout=50)
    soup = BeautifulSoup(html_page, features="html.parser")
    for link in soup.findAll('a'):
        episode = str(link.get("href"))
        if "/staffel-{}/episode-{}".format(season_count, episode_count) in episode:
            episode_count = episode_count + 1
    logging.debug(MODULE_LOGGER_HEAD + "Now leaving Function get_episodes")
    return episode_count - 1

# ------------------------------------------------------- #
#                      classes
# ------------------------------------------------------- #


# ------------------------------------------------------- #
#                       main
# ------------------------------------------------------- #
