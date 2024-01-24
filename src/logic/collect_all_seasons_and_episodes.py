import urllib.request

from bs4 import BeautifulSoup

from src.custom_logging import setup_logger

logger = setup_logger(__name__)


def get_season(url_path):
    logger.debug("Entered get_season.")
    logger.debug("Site URL is: " + url_path)
    counter_seasons = 1
    html_page = urllib.request.urlopen(url_path, timeout=50)
    soup = BeautifulSoup(html_page, features="html.parser")
    for link in soup.findAll('a'):
        seasons = str(link.get("href"))
        if "/staffel-{}".format(counter_seasons) in seasons:
            counter_seasons = counter_seasons + 1
    logger.debug("Now leaving Function get_season")
    return counter_seasons - 1


def get_episodes(url_path, season_count):
    logger.debug("Entered get_episodes")
    url = "{}staffel-{}/".format(url_path, season_count)
    episode_count = 1
    html_page = urllib.request.urlopen(url, timeout=50)
    soup = BeautifulSoup(html_page, features="html.parser")
    for link in soup.findAll('a'):
        episode = str(link.get("href"))
        if "/staffel-{}/episode-{}".format(season_count, episode_count) in episode:
            episode_count = episode_count + 1
    logger.debug("Now leaving Function get_episodes")
    return episode_count - 1


def get_movies(url_path):
    logger.debug("Entered get_movies")
    url = "{}filme/".format(url_path)
    movie_count = 1
    html_page = urllib.request.urlopen(url, timeout=50)
    soup = BeautifulSoup(html_page, features="html.parser")
    for link in soup.findAll('a'):
        movie = str(link.get("href"))
        if "/filme/film-{}".format(movie_count) in movie:
            movie_count = movie_count + 1
    logger.debug("Now leaving Function get_movies")
    return movie_count - 1

# ------------------------------------------------------- #
#                      classes
# ------------------------------------------------------- #


# ------------------------------------------------------- #
#                       main
# ------------------------------------------------------- #
