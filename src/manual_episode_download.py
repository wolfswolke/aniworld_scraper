import os

from src.constants import (episode_override, language, name, output_path,
                           season_override, type_of_media, url, output_root, output_name, cliProvider)
from src.custom_logging import setup_logger
from src.logic.downloader import create_new_download_thread
from src.logic.language import LanguageError
from src.logic.search_for_links import (find_cache_url,
                                        get_redirect_link_by_provider, get_year)


def main():
    logger = setup_logger(__name__)
    print("Starting Manual Episode Download")
    anime_url = "https://aniworld.to/anime/stream/{}/".format(name)

    read_check = os.access('DO_NOT_DELETE.txt', os.R_OK)
    if read_check:
        logger.debug("We have Read Permission.")
    else:
        logger.error("No Read Permission. Please check if you own the Folder and/or have permissions to read.")
        exit()
    write_check = os.access('DO_NOT_DELETE.txt', os.W_OK)
    if write_check:
        logger.debug("We have Write Permission")
    else:
        logger.error("No Write Permission. Please check if you own the Folder and/or have permissions to write.")
        exit()

    site_url = {"serie": "https://s.to", "anime": "https://aniworld.to"}

    year = get_year(url)
    output_path = f"{output_root}/{type_of_media}/{output_name}_({year})"
    os.makedirs(output_path, exist_ok=True)

    link = anime_url + "staffel-{}/episode-{}".format(season_override, episode_override)
    try:
        redirect_link, provider = get_redirect_link_by_provider(site_url[type_of_media], link, language, cliProvider)
    except LanguageError:
        logger.error("Language not found. Please check the language of the show.")
        exit()
    logger.debug("Link to redirect is: " + redirect_link)
    cache_url = find_cache_url(redirect_link, provider)
    logger.debug("{} Cache URL is: ".format(provider) + cache_url)
    file_name = "{}/{} - s{:02}e{:02} - {}.mp4".format(output_path, name, season_override, episode_override, language)
    if os.path.exists(file_name):
        logger.info("Episode {} already downloaded.".format(file_name))
    else:
        logger.info("File not downloaded. Downloading: {}".format(file_name))
        create_new_download_thread(cache_url, file_name, provider)
    print("Downloads may still be running. Please don't close this Window until its done.")
    print("You will know its done once you see your primary prompt string. Example: C:\\XXX or username@hostname:")
