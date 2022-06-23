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

result = aniworld_to_redirect("https://aniworld.to/anime/stream/the-misfit-of-demon-king-academy/staffel-1/episode-11")
print(result)

# vidoza_link = redirect_to_vidoza(result)
# print(vidoza_link)
cache = vidoza_to_cache("https://vidoza.net/embed-y87qfjmgagf1.html")
print(cache)

print("testing_grounds")

