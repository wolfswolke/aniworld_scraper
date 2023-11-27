import logging
import re
import urllib.request
from urllib.error import URLError

from bs4 import BeautifulSoup

from src.logic.language import ProviderError, get_href_by_language

# ------------------------------------------------------- #
#                   definitions
# ------------------------------------------------------- #
MODULE_LOGGER_HEAD = "search_for_links.py ->"
cache_url_attempts = 0

# ------------------------------------------------------- #
#                   global variables
# ------------------------------------------------------- #
VOE_PATTERN = re.compile(r"'hls': '(?P<url>.+)'")
STREAMTAPE_PATTERN = re.compile(r'get_video\?id=[^&\'\s]+&expires=[^&\'\s]+&ip=[^&\'\s]+&token=[^&\'\s]+\'')
# ------------------------------------------------------- #
#                      functions
# ------------------------------------------------------- #


def get_redirect_link_by_provider(site_url, internal_link, language):
    """
    Sets the priority in which downloads are attempted.
    First -> VOE download, if not available...
    Second -> Streamtape download, if not available...
    Third -> Vidoza download

    Parameters:
        site_url (String): serie or anime site.
        internal_link (String): link of the html page of the episode.
        language (String): desired language to download the video file in.

    Returns:
        get_redirect_link(): returns link_to_redirect and provider.
    """
    try:
        return get_redirect_link(site_url, internal_link, language, "VOE")
    except ProviderError:
        try:
            return get_redirect_link(site_url, internal_link, language, "Streamtape")
        except ProviderError:
            return get_redirect_link(site_url, internal_link, language, "Vidoza")


def get_redirect_link(site_url, html_link, language, provider):
    # if you encounter issues with captchas use this line below
    # html_link = open_captcha_window(html_link)
    html_response = urllib.request.urlopen(html_link)
    href_value = get_href_by_language(html_response, language, provider)
    link_to_redirect = site_url + href_value
    logging.debug(MODULE_LOGGER_HEAD + "Link to redirect is: " + link_to_redirect)
    return link_to_redirect, provider
     

def find_cache_url(url, provider):
    global cache_url_attempts
    logging.debug(MODULE_LOGGER_HEAD + "Enterd {} to cache".format(provider))
    try:
        html_page = urllib.request.urlopen(url)
    except URLError as e:
        logging.warning(MODULE_LOGGER_HEAD + f"{e}")
        logging.info(MODULE_LOGGER_HEAD + "Trying again...")
        if cache_url_attempts < 5:
            return find_cache_url(url, provider)
        else:
            logging.error(MODULE_LOGGER_HEAD + "Could not find cache url for {}.".format(provider))
            return 0
    try:
        if provider == "Vidoza":
            soup = BeautifulSoup(html_page, features="html.parser")
            cache_link = soup.find("source").get("src")
        elif provider == "VOE":
            cache_link = VOE_PATTERN.search(html_page.read().decode('utf-8')).group("url")
        elif provider == "Streamtape":
            cache_link = STREAMTAPE_PATTERN.search(html_page.read().decode('utf-8'))
            if cache_link is None:
                return find_cache_url(url, provider)
            cache_link = "https://" + provider + ".com/" + cache_link.group()[:-1]
            logging.debug(MODULE_LOGGER_HEAD + f"This is the found video link of {provider}: {cache_link}")
    except AttributeError:
        logging.info(MODULE_LOGGER_HEAD + "Trying again...")
        if cache_url_attempts < 5:
            cache_url_attempts += 1
            return find_cache_url(url, provider)
        else:
            logging.error(MODULE_LOGGER_HEAD + "Could not find cache url for {}.".format(provider))
            return 0
        
    logging.debug(MODULE_LOGGER_HEAD + "Exiting {} to Cache".format(provider))
    return cache_link

# ------------------------------------------------------- #
#                      classes
# ------------------------------------------------------- #


# ------------------------------------------------------- #
#                       main
# ------------------------------------------------------- #

