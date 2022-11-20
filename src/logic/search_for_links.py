"""

"""
# ------------------------------------------------------- #
#                     imports
# ------------------------------------------------------- #
from bs4 import BeautifulSoup
import urllib.request
from gutils.logging_handle import logger

# ------------------------------------------------------- #
#                   definitions
# ------------------------------------------------------- #
MODULE_LOGGER_HEAD = "search_for_links ->"

# ------------------------------------------------------- #
#                   global variables
# ------------------------------------------------------- #

# ------------------------------------------------------- #
#                      functions
# ------------------------------------------------------- #


def aniworld_to_redirect(aniworld_link):
    counter = 0
    html_page = urllib.request.urlopen(aniworld_link)
    soup = BeautifulSoup(html_page, features="html.parser")
    for link in soup.findAll('a'):
        redirect_to_aniworld = str(link.get("href"))
        if "/redirect/" in redirect_to_aniworld:
            counter = counter + 1
            if counter == 4:
                redirecting_link = "https://aniworld.to" + redirect_to_aniworld
                return redirecting_link


def vidoza_to_cache(vidoza_url):
    logger.debug(MODULE_LOGGER_HEAD + "Enterd Vidoza to cache")
    html_page = urllib.request.urlopen(vidoza_url)
    soup = BeautifulSoup(html_page, features="html.parser")
    for link in soup.findAll('source'):
        cache_link = str(link.get("src"))
        logger.debug(MODULE_LOGGER_HEAD + "Exiting Vidoza to Cache")
        return cache_link

# ------------------------------------------------------- #
#                      classes
# ------------------------------------------------------- #


# ------------------------------------------------------- #
#                       main
# ------------------------------------------------------- #

