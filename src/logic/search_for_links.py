"""

"""
# ------------------------------------------------------- #
#                     imports
# ------------------------------------------------------- #
import re
import urllib.request
from urllib.error import URLError
from logic.language import get_href_by_language
from logic.language import ProviderError
from bs4 import BeautifulSoup
from zk_tools.logging_handle import logger
from logic.captcha import open_captcha_window

# ------------------------------------------------------- #
#                   definitions
# ------------------------------------------------------- #
MODULE_LOGGER_HEAD = "search_for_links.py ->"

# ------------------------------------------------------- #
#                   global variables
# ------------------------------------------------------- #
VOE_PATTERN = re.compile(r"'hls': '(?P<url>.+)'")

# ------------------------------------------------------- #
#                      functions
# ------------------------------------------------------- #


def get_redirect_link(site_url, internal_link, language, provider):
    link_to_redirect = redirect(site_url, internal_link, language, provider)
    logger.debug(MODULE_LOGGER_HEAD + "Link to redirect is: " + link_to_redirect)
    # if you encounter issues with captchas use this line below
    # link_to_redirect = open_captcha_window(link_to_redirect)
    logger.debug(MODULE_LOGGER_HEAD + "Return is: " + link_to_redirect)
    return link_to_redirect, provider


def get_redirect_link_by_provider(site_url, internal_link, language):
    try:
        return get_redirect_link(site_url, internal_link, language, "VOE")
    except ProviderError:
        return get_redirect_link(site_url, internal_link, language, "Vidoza")


def redirect(site_url, html_link, language, provider):
    html_response = urllib.request.urlopen(html_link)
    href_value = get_href_by_language(html_response, language, provider)
    return site_url + href_value
     

def find_cache_url(url, provider):
    logger.debug(MODULE_LOGGER_HEAD + "Enterd {} to cache".format(provider))
    try:
        html_page = urllib.request.urlopen(url)
    except URLError as e:
        logger.warning(MODULE_LOGGER_HEAD + f"{e}")
        logger.info(MODULE_LOGGER_HEAD + "Trying again...")
        return find_cache_url(url, provider)
    if provider == "Vidoza":
        soup = BeautifulSoup(html_page, features="html.parser")
        cache_link = soup.find("source").get("src")
    elif provider == "VOE":
        cache_link = VOE_PATTERN.search(html_page.read().decode('utf-8')).group("url")
    logger.debug(MODULE_LOGGER_HEAD + "Exiting {} to Cache".format(provider))
    return cache_link

# ------------------------------------------------------- #
#                      classes
# ------------------------------------------------------- #


# ------------------------------------------------------- #
#                       main
# ------------------------------------------------------- #

