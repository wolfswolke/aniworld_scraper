import base64
import json
import re
import m3u8
import requests
import urllib.request
from urllib.error import URLError
from urllib.parse import urljoin

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
# --------------------------------------------------------#
#       Get highest Quality from Videolist                #
# --------------------------------------------------------#


def get_highest_quality_stream(m3u8_master_url):
    response = requests.get(m3u8_master_url)
    response.raise_for_status()

    base_url = m3u8_master_url.rsplit("/", 1)[0] + "/"
    playlist = m3u8.loads(response.text)

    best_stream = max(
        playlist.playlists,
        key=lambda x: x.stream_info.resolution[1] if x.stream_info.resolution else 0
    )

    best_uri = urljoin(base_url, best_stream.uri)
    resolution = best_stream.stream_info.resolution  # ex. (1280, 720)

    return best_uri, resolution[1]  # Return URL and Quality


# --------------------------------------------------------#
#       NEW VOE DEOBFUSCATION FUNCTION 2025-05-01         #
# --------------------------------------------------------#

def find_script_element_voenew(raw_html):
    soup = BeautifulSoup(raw_html, features="html.parser")
    MKGMa_pattern = r'MKGMa="(.*?)"'
    match = re.search(MKGMa_pattern, str(soup), re.DOTALL)

    if not match:
        logger.info("[*] Searching for new MKGMa application/json ...")
        MKGMa_pattern=r'<script type="application/json">.*\[(.*?)\]</script>'
        match = re.search(MKGMa_pattern, str(soup), re.DOTALL)
    if match:
        raw_MKGMa = match.group(1)

        def rot13_decode(s: str) -> str:
            result = []
            for c in s:
                if 'A' <= c <= 'Z':
                    result.append(chr((ord(c) - ord('A') + 13) % 26 + ord('A')))
                elif 'a' <= c <= 'z':
                    result.append(chr((ord(c) - ord('a') + 13) % 26 + ord('a')))
                else:
                    result.append(c)
            return ''.join(result)

        def shift_characters(s: str, offset: int) -> str:
            return ''.join(chr(ord(c) - offset) for c in s)

        try:
            step1 = rot13_decode(raw_MKGMa)
            step2 = step1.replace('_', '')
            step3 = base64.b64decode(step2).decode('utf-8')
            step4 = shift_characters(step3, 3)
            step5 = step4[::-1]

            decoded = base64.b64decode(step5).decode('utf-8')
            try:
                parsed_json = json.loads(decoded)
                if 'source' in parsed_json:
                    try:
                        best_quality_url, res_height = get_highest_quality_stream(parsed_json['source'])
                        source_json = {"hls": best_quality_url}
                        logger.info(f"[+] Choosed best Quality {res_height}p in .m3u8")
                    except Exception as e:
                        logger.error(f"[!] Error while parsing .m3u8-File: {e}")
                        source_json = {"hls": parsed_json['source']}  # fallback to master.m3u8
                elif 'direct_access_url' in parsed_json:
                    source_json = {"mp4": parsed_json['direct_access_url']}
                    logger.info("[+] Found direct .mp4 URL in JSON (no .m3u8 fallback available).")
            except json.JSONDecodeError:
                logger.error("[-] Decoded string is not valid JSON. Attempting fallback regex search...")

                mp4_match = re.search(r'(https?://[^\s"]+\.mp4[^\s"]*)', decoded)
                m3u8_match = re.search(r'(https?://[^\s"]+\.m3u8[^\s"]*)', decoded)

                if mp4_match:
                    source_json = {"mp4": mp4_match.group(1)}
                    logger.info("[+] Found base64 encoded MP4 URL.")
                elif m3u8_match:
                    source_json = {"hls": m3u8_match.group(1)}
                    logger.info("[+] Found base64 encoded HLS (m3u8) URL.")
        except Exception as e:
            logger.error(f"[-] Error while decoding MKGMa string: {e}")
        try:
            if "mp4" in source_json:
                link = source_json["mp4"]
                # Check if the link is base64 encoded
                if isinstance(link, str) and (link.startswith("eyJ") or re.match(r'^[A-Za-z0-9+/=]+$', link)):
                    try:
                        link = base64.b64decode(link).decode("utf-8")
                        logger.info("[+] Successfully decoded base64 MP4 URL")
                    except Exception as e:
                        logger.error(f"[!] Failed to decode base64: {e}")

                # Ensure the link is a complete URL
                if link.startswith("//"):
                    link = "https:" + link

                return link

            elif "hls" in source_json:
                link = source_json["hls"]
                # Check if the link is base64 encoded
                if isinstance(link, str) and (link.startswith("eyJ") or re.match(r'^[A-Za-z0-9+/=]+$', link)):
                    try:
                        link = base64.b64decode(link).decode("utf-8")
                        logger.info("[+] Successfully decoded base64 HLS URL")
                    except Exception as e:
                        logger.error(f"[!] Failed to decode base64: {e}")

                # Ensure the link is a complete URL
                if link.startswith("//"):
                    link = "https:" + link

                return link

            else:
                logger.error("[!] Could not find downloadable URL. The site might have changed.")
                logger.error(f"Available keys in source_json: {list(source_json.keys())}")
                for key, value in source_json.items():
                    logger.error(f"{key}: {value}")
        except KeyError as e:
            logger.error(f"[!] KeyError: {e}")
            logger.error("[!] Could not find downloadable URL. The site might have changed.")
            logger.error(f"Available keys in source_json: {list(source_json.keys())}")

    return None

# --------------------------------------------------------#
#       NEW VOE DEOBFUSCATION FUNCTION 2025-05-01 END     #
# --------------------------------------------------------#

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
        if "11004" in str(e):
            logger.error("DNS Error. Please check your DNS settings.")
            return 0
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
            ## New Version of VOE 2025-05-01
            cache_url = find_script_element_voenew(html_page)
            if cache_url:
                return cache_url
            else:
                logger.info(f"Older VOE page. Trying a different methode...")
            ##
            # new Version of VOE uses a b64 encoded block which is also backwards.
            try:
                b64_match = re.search(r"var a168c='([^']+)'", html_page)
                if b64_match:
                    logger.debug("Found b64 encoded block. Decoding...")
                    html_page = base64.b64decode(b64_match.group(1)).decode('utf-8')[::-1]
                    html_page = json.loads(html_page)
                    html_page = html_page["source"]
                    return html_page
            except AttributeError:
                logger.info("Could not find b64 encoded block. Older VOE Version")

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

