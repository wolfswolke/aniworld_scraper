"""

"""
# ------------------------------------------------------- #
#                     imports
# ------------------------------------------------------- #
from gutils.logging_handle import logger

from logic.search_for_links import aniworld_to_redirect
from logic.search_for_links import redirect_to_vidoza
from logic.search_for_links import vidoza_to_cache
from logic.collect_all_seasons_and_episods import get_season
from logic.collect_all_seasons_and_episods import get_episodes
from logic.downloader import downloader

# ------------------------------------------------------- #
#                   definitions
# ------------------------------------------------------- #
APP_VERSION = "v01-00-05"
MODULE_LOGGER_HEAD = "start_app -> "

# ------------------------------------------------------- #
#                   global variables
# ------------------------------------------------------- #
anime_name = "the-rising-of-the-shield-hero"
anime_url = "https://aniworld.to/anime/stream/{}/".format(anime_name)


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
    try:
        logger.info("------------- AniWorldScraper {} started ------------".format(APP_VERSION))

        seasons = get_season(anime_name)
        logger.debug(MODULE_LOGGER_HEAD + "We have this many seasons: {}".format(seasons))
        for season in range(int(seasons)):
            season = season + 1
            episode_count = get_episodes(season, anime_name)
            logger.debug(MODULE_LOGGER_HEAD + "Season {} has {} Episodes.".format(season, episode_count))
            for episode in range(int(episode_count)):
                episode = episode + 1
                link = anime_url + "staffel-{}/episode-{}".format(season, episode)
                link_to_redirect = aniworld_to_redirect(link)

                # PLACE HOLDER FOR REDIRECT TO VIDOZA
                # vidoza_link = redirect_to_vidoza(link_to_redirect)

                # WORKING
                # vidoza_cache_url = vidoza_to_cache(vidoza_link)

                # WORKING
                # file_name = "S{}-E{}-{}.mp4".format(season, episode, anime_name)
                # downloader(vidoza_cache_url, file_name)
    except Exception as e:
        logger.error(MODULE_LOGGER_HEAD + "----------")
        logger.error(MODULE_LOGGER_HEAD + f"Exception: {e}")
        logger.error(MODULE_LOGGER_HEAD + "----------")

    except KeyboardInterrupt:
        logger.info("-----------------------------------------------------------")
        logger.info("            AniWorldScraper Stopped")
        logger.info("-----------------------------------------------------------")
