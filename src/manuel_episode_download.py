from gutils.logging_handle import logger

import os

from logic.search_for_links import aniworld_to_redirect
from logic.search_for_links import vidoza_to_cache
from logic.downloader import create_new_download_thread
from logic.captcha import open_captcha_window

MODULE_LOGGER_HEAD = "manuel_episode_download.py -> "
anime_name = "Anime-Name-Goes-Here"
anime_url = "https://aniworld.to/anime/stream/{}/".format(anime_name)
season = 0
episode = 0


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

link = anime_url + "staffel-{}/episode-{}".format(season, episode)
link_to_redirect = aniworld_to_redirect(link)
logger.debug(MODULE_LOGGER_HEAD + "Link to redirect is: " + link_to_redirect)
captcha_link = open_captcha_window(link_to_redirect)
logger.debug(MODULE_LOGGER_HEAD + "Return is: " + captcha_link)
vidoza_cache_url = vidoza_to_cache(captcha_link)
logger.debug(MODULE_LOGGER_HEAD + "Vidoza Cache URL is: " + vidoza_cache_url)
file_name = "S{}-E{}-{}.mp4".format(season, episode, anime_name)
create_new_download_thread(vidoza_cache_url, file_name)
