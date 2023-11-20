import logging

import os

from logic.search_for_links import get_redirect_link_by_provider
from logic.search_for_links import find_cache_url
from logic.downloader import create_new_download_thread

from constants import output_path, season_override, episode_override, language, name, type_of_media

MODULE_LOGGER_HEAD = "manuel_episode_download.py -> "
anime_url = "https://aniworld.to/anime/stream/{}/".format(name)

read_check = os.access('DO_NOT_DELETE.txt', os.R_OK)
if read_check:
    logging.debug("We have Read Permission")
else:
    logging.error("No Read Permission. Please check if you own the Folder and/or have permissions to read.")
    exit()
write_check = os.access('DO_NOT_DELETE.txt', os.W_OK)
if write_check:
    logging.debug("We have Write Permission")
else:
    logging.error("No Write Permission. Please check if you own the Folder and/or have permissions to write.")
    exit()
if os.path.exists(output_path):
    logging.debug(MODULE_LOGGER_HEAD + "Output Path exists.")
else:
    logging.info(MODULE_LOGGER_HEAD + "Output path does not exist. Creating now...")
    os.mkdir(output_path)
site_url = {"serie": "https://s.to", "anime": "https://aniworld.to"}
link = anime_url + "staffel-{}/episode-{}".format(season_override, episode_override)
redirect_link, provider = get_redirect_link_by_provider(site_url[type_of_media], link, language)
logging.debug(MODULE_LOGGER_HEAD + "Link to redirect is: " + redirect_link)
cache_url = find_cache_url(redirect_link, provider)
logging.debug(MODULE_LOGGER_HEAD + "{} Cache URL is: ".format(provider) + cache_url)
file_name = "{}/S{}-E{}-{}.mp4".format(name, season_override, episode_override, name)
if os.path.exists(file_name):
    logging.info(MODULE_LOGGER_HEAD + "Episode {} already downloaded.".format(file_name))
else:
    logging.info(MODULE_LOGGER_HEAD + "File not downloaded. Downloading: {}".format(file_name))
    create_new_download_thread(cache_url, file_name, provider)
print("Downloads may still be running. Please dont close this Window until its done")
print("You will know its done once you see your primary prompt string. Example: C:\\XXX or username@hostname:")
