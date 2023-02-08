"""

"""
# ------------------------------------------------------- #
#                     imports
# ------------------------------------------------------- #
from bs4 import BeautifulSoup
import urllib.request

from zk_tools.logging_handle import logger

# ------------------------------------------------------- #
#                   definitions
# ------------------------------------------------------- #
MODULE_LOGGER_HEAD = "collect_all_seasons_and_episods -> "

# ------------------------------------------------------- #
#                   global variables
# ------------------------------------------------------- #

# ------------------------------------------------------- #
#                      functions
# ------------------------------------------------------- #


def get_season(anime_name):
    logger.debug(MODULE_LOGGER_HEAD + "Entert get_season.")
    anime_url = "https://aniworld.to/anime/stream/{}/".format(anime_name)
    logger.debug(MODULE_LOGGER_HEAD + "Anime name is: " + anime_name)
    logger.debug(MODULE_LOGGER_HEAD + "Anime URL is: " + anime_url)
    counter_seasons = 1
    html_page = urllib.request.urlopen(anime_url, timeout=50)
    soup = BeautifulSoup(html_page, features="html.parser")
    for link in soup.findAll('a'):
        seasons = str(link.get("href"))
        if "/anime/stream/{}/staffel-{}".format(anime_name, counter_seasons) in seasons:
            counter_seasons = counter_seasons + 1
    logger.debug(MODULE_LOGGER_HEAD + "Now leaving Function get_season")
    return counter_seasons - 1


def get_episodes(season_count, anime_name):
    logger.debug(MODULE_LOGGER_HEAD + "Enterd get_episodes")
    anime_url = "https://aniworld.to/anime/stream/{}/staffel-{}/".format(anime_name, season_count)
    episode_count = 1
    html_page = urllib.request.urlopen(anime_url, timeout=50)
    soup = BeautifulSoup(html_page, features="html.parser")
    for link in soup.findAll('a'):
        episode = str(link.get("href"))
        if "/anime/stream/{}/staffel-{}/episode-{}".format(anime_name, season_count, episode_count) in episode:
            episode_count = episode_count + 1
    logger.debug(MODULE_LOGGER_HEAD + "Now leaving Function get_episodes")
    return episode_count - 1

# ------------------------------------------------------- #
#                      classes
# ------------------------------------------------------- #


# ------------------------------------------------------- #
#                       main
# ------------------------------------------------------- #
