import base64
import re
import urllib.request
from urllib.error import URLError

from bs4 import BeautifulSoup

from src.custom_logging import setup_logger
from src.logic.language import ProviderError, get_href_by_language
from src.constants import (provider_priority)

logger = setup_logger(__name__)

# ------------------------------------------------------- #
#                   definitions
# ------------------------------------------------------- #
cache_url_attempts = 0

# ------------------------------------------------------- #
#                   global variables
# ------------------------------------------------------- #
VOE_PATTERNS = [re.compile(r"'hls': '(?P<url>.+)'"),
                re.compile(r'prompt\("Node",\s*"(?P<url>[^"]+)"'),
                re.compile(r"window\.location\.href = '(?P<url>[^']+)'")]
STREAMTAPE_PATTERN = re.compile(r'get_video\?id=[^&\'\s]+&expires=[^&\'\s]+&ip=[^&\'\s]+&token=[^&\'\s]+\'')

# ------------------------------------------------------- #
#                      functions
# ------------------------------------------------------- #


def get_year(url):
    """
    Get the year of the show.

    Parameters:
        url (String): url of the show.

    Returns:
        year (String): year of the show.
    """
    try:
        html_page = urllib.request.urlopen(url)
        soup = BeautifulSoup(html_page, features="html.parser")
        year = soup.find("span", {"itemprop": "startDate"}).text
        return year
    except AttributeError:
        logger.error("Could not find year of the show.")
        return 0


def get_redirect_link_by_provider(site_url, internal_link, language, provider):
    """
    Sets the priority in which downloads are attempted.
    First -> VOE download, if not available...
    Second -> Streamtape download, if not available...
    Third -> Vidoza download
    Fourth -> SpeedFiles download

    Parameters:
        site_url (String): serie or anime site.
        internal_link (String): link of the html page of the episode.
        language (String): desired language to download the video file in.
        provider (String): define the provider to use.

    Returns:
        get_redirect_link(): returns link_to_redirect and provider.
    """
    local_provider_priority = provider_priority.copy()
    local_provider_priority.remove(provider)
    try:
        return get_redirect_link(site_url, internal_link, language, provider)
    except ProviderError:
        logger.info(f"Provider {provider} failed. Trying {local_provider_priority[0]} next.")
        try:
            return get_redirect_link(site_url, internal_link, language, local_provider_priority[0])
        except ProviderError:
            logger.info(f"Provider {local_provider_priority[0]} failed. Trying {local_provider_priority[1]} next.")
            return get_redirect_link(site_url, internal_link, language, local_provider_priority[1])


def get_redirect_link(site_url, html_link, language, provider):
    html_response = urllib.request.urlopen(html_link)
    href_value = get_href_by_language(html_response, language, provider)
    link_to_redirect = site_url + href_value
    logger.debug("Link to redirect is: " + link_to_redirect)
    return link_to_redirect, provider
     

def find_cache_url(url, provider):
    global cache_url_attempts
    logger.debug("Enterd {} to cache".format(provider))
    try:
        html_page = urllib.request.urlopen(url)
    except URLError as e:
        logger.warning(f"{e}")
        logger.info("Trying again to read HTML Element...")
        if cache_url_attempts < 5:
            return find_cache_url(url, provider)
        else:
            logger.error("Could not find cache url HTML for {}.".format(provider))
            return 0
    try:
        if provider == "Vidoza":
            soup = BeautifulSoup(html_page, features="html.parser")
            cache_link = soup.find("source").get("src")
        elif provider == "SpeedFiles":
            cache_link = re.search(r'src="([^"]+)"', html_page.read().decode('utf-8')).group(1)
            logger.debug(f"Link: {cache_link}")
            if "store_access" in cache_link:
                logger.info("Found SpeedFiles mp4 Link!")
                return cache_link
        elif provider == "VOE":
            html_page = html_page.read().decode('utf-8')
            for VOE_PATTERN in VOE_PATTERNS:
                match = VOE_PATTERN.search(html_page)
                if match:
                    if match.group(0).startswith("window.location.href"):
                        logger.info("Found window.location.href. Redirecting...")
                        logger.debug(f"Redirecting to {match.group(1)}")
                        return find_cache_url(match.group(1), provider)
                    cache_link = match.group(1)
                    cache_link = base64.b64decode(cache_link).decode('utf-8')
                    if cache_link and cache_link.startswith("https://"):
                        return cache_link
            logger.error("Could not find cache url for {}.".format(provider))
            return 0
        elif provider == "Streamtape":
            cache_link = STREAMTAPE_PATTERN.search(html_page.read().decode('utf-8'))
            if cache_link is None:
                return find_cache_url(url, provider)
            cache_link = "https://" + provider + ".com/" + cache_link.group()[:-1]
            logger.debug(f"This is the found video link of {provider}: {cache_link}")
    except AttributeError as e:
        logger.error(f"ERROR: {e}")
        logger.info("Trying again...")
        if cache_url_attempts < 5:
            cache_url_attempts += 1
            return find_cache_url(url, provider)
        else:
            logger.error("Could not find cache url for {}.".format(provider))
            return 0
        
    logger.debug("Exiting {} to Cache".format(provider))
    return cache_link

# ------------------------------------------------------- #
#                      classes
# ------------------------------------------------------- #


# ------------------------------------------------------- #
#                       main
# ------------------------------------------------------- #

