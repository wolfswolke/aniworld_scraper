from zk_tools.logging_handle import logger

import os

from logic.search_for_links import get_redirect_link_by_provider
from logic.search_for_links import find_cache_url
from logic.downloader import create_new_download_thread

MODULE_LOGGER_HEAD = "manuel_episode_download.py -> "
anime_name = "Anime-Name-Goes-Here"
anime_url = "https://aniworld.to/anime/stream/{}/".format(anime_name)
season = 0
episode = 0
output_path = anime_name
lanugage = "Deutsch" # "Deutsch", "Ger-Sub" or "English
type_of_media = "anime" # choose 'serie' or 'anime'


def setup_logging(debug_level):
    logger.set_logging_level(debug_level)
    logger.set_cmd_line_logging_output()
    logger.add_global_except_hook()


setup_logging("info")
read_check = os.access('DO_NOT_DELETE.txt', os.R_OK)
if read_check:
    logger.debug("We have Read Permission")
else:
    logger.error("No Read Permission. Please check if you own the Folder and/or have permissions to read.")
    exit()
write_check = os.access('DO_NOT_DELETE.txt', os.W_OK)
if write_check:
    logger.debug("We have Write Permission")
else:
    logger.error("No Write Permission. Please check if you own the Folder and/or have permissions to write.")
    exit()
if os.path.exists(output_path):
    logger.debug(MODULE_LOGGER_HEAD + "Output Path exists.")
else:
    logger.info(MODULE_LOGGER_HEAD + "Output path does not exist. Creating now...")
    os.mkdir(output_path)
site_url = {"serie": "https://s.to", "anime": "https://aniworld.to"}
link = anime_url + "staffel-{}/episode-{}".format(season, episode)
redirect_link, provider = get_redirect_link_by_provider(site_url[type_of_media], link, lanugage)
logger.debug(MODULE_LOGGER_HEAD + "Link to redirect is: " + redirect_link)
cache_url = find_cache_url(redirect_link, provider)
logger.debug(MODULE_LOGGER_HEAD + "{} Cache URL is: ".format(provider) + cache_url)
file_name = "{}/S{}-E{}-{}.mp4".format(anime_name, season, episode, anime_name)
if os.path.exists(file_name):
    logger.info(MODULE_LOGGER_HEAD + "Episode {} already downloaded.".format(file_name))
else:
    logger.info(MODULE_LOGGER_HEAD + "File not downloaded. Downloading: {}".format(file_name))
    create_new_download_thread(cache_url, file_name, provider)
print("Downloads may still be running. Please dont close this Window until its done")
print("You will know its done once you see your primary prompt string. Example: C:\\XXX or username@hostname:")
