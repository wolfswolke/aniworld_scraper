import os
import time
import re

from src.constants import (APP_VERSION, ddos_protection_calc, ddos_wait_timer, output_path, output_root)
from src.custom_logging import setup_logger
from src.logic.downloader import create_new_download_thread
from src.logic.language import LanguageError
from src.logic.search_for_links import (find_cache_url,
                                        get_redirect_link_by_provider)
from src.failures import write_fails, append_failure, failures
from src.successes import write_succs

logger = setup_logger(__name__)

# ------------------------------------------------------- #
#                       main
# ------------------------------------------------------- #

def main():
    ddos_start_value = 0

    logger.info("------------- AnimeSerienScraper {} started ------------".format(APP_VERSION))

    read_check = os.access('DO_NOT_DELETE.txt', os.R_OK)
    if read_check:
        logger.debug("We have Read Permission")
    else:
        logger.error("No Read Permission. Please check if you own the Folder and/or have "
                     "permissions to read.")
        exit()
    write_check = os.access('DO_NOT_DELETE.txt', os.W_OK)
    if write_check:
        logger.debug("We have Write Permission")
    else:
        logger.error("No Write Permission. Please check if you own the Folder and/or have "
                     "permissions to write.")
        exit()

    if not os.path.exists(output_root):
        logger.info("Output folder does not exist. Creating it now.")
        os.makedirs(output_root, exist_ok=True)

    os.makedirs(output_path, exist_ok=True)

    threadpool = []

    if len(failures) == 0:
        logger.info("No failures detected.")
        exit()

    for failure in failures:
        try:
            pattern = re.compile(r"^\[(?P<utctime>\d+-\d+-\d+T\d+:\d+:\d+.\d+\+\d+:\d+)\]\W(?P<filename>.*\.mp4)(\W-\W\[(?P<params>.*)\])?(\W-\W(?P<link>.*))$")
            utcTime = pattern.search(failure).group('utctime')
            file_name = pattern.search(failure).group('season')
            matches = pattern.search(failure).group('matches')
        except AttributeError:
            continue
        if not matches:
            cache_url = pattern.search(failure).group('link')
        else:
            link = pattern.search(failure).group('link')
            params = matches.split("::")
            site_url = params[0]
            language = params[1]
            provider = params[2]

            try:
                redirect_link, provider = get_redirect_link_by_provider(site_url, link, language, provider)
            except LanguageError:
                append_failure(file_name, f"[{site_url}::{language}::{provider}] - {link}")
                continue
        
            if ddos_start_value < ddos_protection_calc:
                logger.debug("Entered DDOS var check and starting new downloader.")
                ddos_start_value += 1
            else:
                logger.info("Started {} Downloads. Waiting for {} Seconds to not trigger DDOS"
                            "Protection.".format(ddos_protection_calc, ddos_wait_timer))
                time.sleep(ddos_wait_timer)
                ddos_start_value = 1

            cache_url = find_cache_url(redirect_link, provider)
            try:
              pattern = re.compile(r"s(?P<season>\d+)e(?P<episode>\d+)")
              season = pattern.search(file_name).group('season')
              episode = pattern.search(file_name).group('episode')
            except AttributeError:
              season = 'None'
              episode = 'None'

            if cache_url == 0:
                logger.error(f"Could not find cache url for {provider} on {season}, {episode}.")
                continue
        
        logger.debug("{} Cache URL is: ".format(provider) + cache_url)
        threadpool.append(create_new_download_thread(cache_url, file_name, provider))

    for thread in threadpool:
        thread.join()

    write_succs()
    write_fails()
