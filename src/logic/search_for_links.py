import re
import time
import random

from urllib.request import urlopen, Request
from urllib.error import URLError
from urllib.parse import urlparse

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
                re.compile(r"window\.location\.href = '([^']+)'")]
DOODSTREAM_PATTERN_URL = re.compile(r"'(?P<url>/pass_md5/[^'.*]*)'")
DOODSTREAM_PATTERN_TOKEN = re.compile(r"token=(?P<token>[^&.*]*)&")
STREAMTAPE_PATTERN = re.compile(r'get_video\?id=[^&\'\s]+&expires=[^&\'\s]+&ip=[^&\'\s]+&token=[^&\'\s]+\'')

# ------------------------------------------------------- #
#                      functions
# ------------------------------------------------------- #

def current_milli_time():
    return round(time.time() * 1000)

def create_doodstream_url_hash(count=10):
    return ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789') for i in range(count))

def get_year(url):
    """
    Get the year of the show.

    Parameters:
        url (String): url of the show.

    Returns:
        year (String): year of the show.
    """
    try:
        html_page = urlopen(url)
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
    local_provider_priority.insert(0, provider)

    logger.info(f"Trying {provider} first.")
    for index, provider in enumerate(local_provider_priority):
        try:
            return get_redirect_link(site_url, internal_link, language, provider)
        except ProviderError:
            if index + 1 < len(local_provider_priority):
                logger.info(f"Provider {provider} failed. Trying {local_provider_priority[index]} next.")
                continue
    raise ProviderError


def get_redirect_link(site_url, html_link, language, provider):
    # if you encounter issues with captchas use this line below
    # html_link = open_captcha_window(html_link)
    html_response = urlopen(html_link)
    href_value = get_href_by_language(html_response, language, provider)
    link_to_redirect = site_url + href_value
    logger.debug("Link to redirect is: " + link_to_redirect)
    return link_to_redirect, provider
     

def find_cache_url(url, provider):
    global cache_url_attempts
    logger.debug("Enterd {} to cache {}".format(provider, url))
    try:
        req = Request(url)
        req.add_header("User-Agent", "Mozilla/5.0")
        html_page = urlopen(req)
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
        elif provider == "VOE":
            html_page = html_page.read().decode('utf-8')
            for VOE_PATTERN in VOE_PATTERNS:
                match = VOE_PATTERN.search(html_page)
                if match:
                    if match.group(0).startswith("window.location.href"):
                        logger.info("Found window.location.href. Redirecting...")
                        return find_cache_url(match.group(1), provider)
                    cache_link = match.group(1)
                    if cache_link and cache_link.startswith("https://"):
                        return cache_link
            logger.error("Could not find cache url for {}.".format(provider))
            return 0
        elif provider == "Doodstream":
            referer = html_page.url
            html_page = html_page.read().decode('utf-8')
            match_url = DOODSTREAM_PATTERN_URL.search(html_page)
            match_token = DOODSTREAM_PATTERN_TOKEN.search(html_page)
            if match_url and match_token:
                parsed_url = urlparse(referer)
                prefetch_req = Request(f"{parsed_url.scheme}://{parsed_url.netloc}" + match_url.group('url'))
                logger.debug(f"Prefetching {prefetch_req.full_url} for {referer}")
                prefetch_req.add_header("Referer", referer)
                prefetch_req.add_header("User-Agent", "Mozilla/5.0")
                req_body = urlopen(prefetch_req).read().decode('utf-8')
                hash = create_doodstream_url_hash()
                cache_link = f"{req_body}{hash}?token={match_token.group('token')}&expiry={current_milli_time()}"
                logger.debug(f"Video URL: {cache_link}")
                return cache_link
            logger.debug(f"This is the found video link of {provider}: {cache_link}")
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

