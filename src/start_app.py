"""

"""
# ------------------------------------------------------- #
#                     imports
# ------------------------------------------------------- #
from gutils.logging_handle import logger

import os
import time

from logic.search_for_links import aniworld_to_redirect
from logic.search_for_links import vidoza_to_cache
from logic.collect_all_seasons_and_episods import get_season
from logic.collect_all_seasons_and_episods import get_episodes
from logic.downloader import create_new_download_thread
from logic.captcha import open_captcha_window

# ------------------------------------------------------- #
#                   definitions
# ------------------------------------------------------- #
APP_VERSION = "v01-01-00"
MODULE_LOGGER_HEAD = "start_app -> "

# ------------------------------------------------------- #
#                   global variables
# ------------------------------------------------------- #
anime_name = "Anime-Name-Goes-Here"
anime_url = "https://aniworld.to/anime/stream/{}/".format(anime_name)
season_override = 0  # 0 = no override. 1 = season 1. etc...
ddos_protection_calc = 5
ddos_wait_timer = 60
ddos_start_value = 0


# ------------------------------------------------------- #
#                      functions
# ------------------------------------------------------- #
def setup_logging(debug_level):
    logger.set_logging_level(debug_level)
    logger.set_cmd_line_logging_output()
    logger.add_global_except_hook()

# ------------------------------------------------------- #
#                      classes
# ------------------------------------------------------- #


# ------------------------------------------------------- #
#                       main
# ------------------------------------------------------- #
if __name__ == "__main__":
    setup_logging("info")
    try:
        logger.info("------------- AniWorldScraper {} started ------------".format(APP_VERSION))

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

        if anime_name == "Anime-Name-Goes-Here":
            logger.error(MODULE_LOGGER_HEAD + "Anime Name is Default. Please reade readme before starting.")
            exit()

        if season_override == 0:
            logger.info(MODULE_LOGGER_HEAD + "No Season override detected.")
            seasons = get_season(anime_name)
            logger.info(MODULE_LOGGER_HEAD + "We have this many seasons: {}".format(seasons))
        else:
            logger.info(MODULE_LOGGER_HEAD + "Season Override detected. Override set to: {}".format(season_override))
            seasons = 1

        for season in range(int(seasons)):
            season = season + 1
            if season_override == 0:
                episode_count = get_episodes(season, anime_name)
                logger.info(MODULE_LOGGER_HEAD + "Season {} has {} Episodes.".format(season, episode_count))
            else:
                episode_count = get_episodes(season_override, anime_name)
                logger.info(MODULE_LOGGER_HEAD + "Season {} has {} Episodes.".format(season_override, episode_count))

            for episode in range(int(episode_count)):
                episode = episode + 1

                if season_override == 0:
                    link = anime_url + "staffel-{}/episode-{}".format(season, episode)
                else:
                    link = anime_url + "staffel-{}/episode-{}".format(season_override, episode)

                link_to_redirect = aniworld_to_redirect(link)

                logger.debug(MODULE_LOGGER_HEAD + "Link to redirect is: " + link_to_redirect)
                captcha_link = open_captcha_window(link_to_redirect)
                logger.debug(MODULE_LOGGER_HEAD + "Return is: " + captcha_link)
                vidoza_cache_url = vidoza_to_cache(captcha_link)
                logger.debug(MODULE_LOGGER_HEAD + "Vidoza Cache URL is: " + vidoza_cache_url)
                if season_override == 0:
                    file_name = "S{}-E{}-{}.mp4".format(season, episode, anime_name)
                else:
                    file_name = "S{}-E{}-{}.mp4".format(season_override, episode, anime_name)
                logger.info(MODULE_LOGGER_HEAD + "File name will be: " + file_name)
                if ddos_start_value < ddos_protection_calc:
                    logger.debug(MODULE_LOGGER_HEAD + "Entered DDOS var check and starting new downloader.")
                    ddos_start_value = ddos_start_value + 1
                    create_new_download_thread(vidoza_cache_url, file_name)
                else:
                    logger.info(MODULE_LOGGER_HEAD + "Started {} Downloads. Waiting for {} Seconds to not trigger DDOS"
                                                     "Protection.".format(ddos_protection_calc, ddos_wait_timer))
                    time.sleep(ddos_wait_timer)
                    create_new_download_thread(vidoza_cache_url, file_name)
                    ddos_start_value = 1

    except Exception as e:
        logger.error(MODULE_LOGGER_HEAD + "----------")
        logger.error(MODULE_LOGGER_HEAD + f"Exception: {e}")
        logger.error(MODULE_LOGGER_HEAD + "----------")

    except KeyboardInterrupt:
        logger.info("-----------------------------------------------------------")
        logger.info("            AniWorldScraper Stopped")
        logger.info("-----------------------------------------------------------")
        logger.info("Downloads may still be running. Please dont close this Window until its done.")
        logger.info("You will know its done once you see your primary prompt string. Example: C:\\XXX or username@hostname:")
