from logic.search_for_links import aniworld_to_redirect
from logic.search_for_links import redirect_to_vidoza
from logic.search_for_links import vidoza_to_cache
from logic.collect_all_seasons_and_episods import get_season
from logic.collect_all_seasons_and_episods import get_episodes

anime_name = "the-rising-of-the-shield-hero"
anime_url = "https://aniworld.to/anime/stream/{}/".format(anime_name)

# get all Seasons.
seasons = get_season(anime_name)
print("We have this many seasons: {}".format(seasons))
for season in range(int(seasons)):
    season = season + 1
    episode_count = get_episodes(season, anime_name)
    print("Season {} has {} Episodes.".format(season, episode_count))
    for episode in range(int(episode_count)):
        episode = episode + 1
        link = anime_url + "staffel-{}/episode-{}".format(season, episode)
        link_to_redirect = aniworld_to_redirect(link)

        # PLACE HOLDER FOR REDIRECT TO VIDOZA
        # vidoza_link = redirect_to_vidoza(result)
        # print(vidoza_link)

        test_vidoza_link = "https://vidoza.net/embed-y87qfjmgagf1.html"
        cache = vidoza_to_cache(test_vidoza_link)
        print(cache)
