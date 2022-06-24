from bs4 import BeautifulSoup
import urllib.request


def get_season(anime_name):
    anime_url = "https://aniworld.to/anime/stream/{}/".format(anime_name)
    counter_seasons = 1
    html_page = urllib.request.urlopen(anime_url)
    soup = BeautifulSoup(html_page, features="html.parser")
    for link in soup.findAll('a'):
        seasons = str(link.get("href"))
        if "/anime/stream/{}/staffel-{}".format(anime_name, counter_seasons) in seasons:
            counter_seasons = counter_seasons + 1
    return counter_seasons - 1


def get_episodes(season_count, anime_name):
    anime_url = "https://aniworld.to/anime/stream/{}/staffel-{}/".format(anime_name, season_count)
    episode_count = 1
    html_page = urllib.request.urlopen(anime_url)
    soup = BeautifulSoup(html_page, features="html.parser")
    for link in soup.findAll('a'):
        episode = str(link.get("href"))
        if "/anime/stream/{}/staffel-{}/episode-{}".format(anime_name, season_count, episode_count) in episode:
            episode_count = episode_count + 1
    return episode_count - 1
