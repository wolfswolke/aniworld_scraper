import requests as requests
from bs4 import BeautifulSoup
import urllib.request


def aniworld_to_redirect(aniworld_link):
    counter = 0
    html_page = urllib.request.urlopen(aniworld_link)
    soup = BeautifulSoup(html_page, features="html.parser")
    for link in soup.findAll('a'):
        redirect_to_aniworld = str(link.get("href"))
        if "/redirect/" in redirect_to_aniworld:
            counter = counter + 1
            if counter == 4:
                redirecting_link = "https://aniworld.to" + redirect_to_aniworld
                return redirecting_link


def redirect_to_vidoza(aniworld_link):
    # cant get past redirect
    counter = 0
    html_page = urllib.request.urlopen(aniworld_link)
    print(html_page)
    soup = BeautifulSoup(html_page, features="html.parser")
    for link in soup.findAll('a'):
        print(link)
        redirect_to_cache = str(link.get("video"))
        print(redirect_to_cache)
        if "/redirect/" in redirect_to_cache:
            counter = counter + 1
            if counter == 10000000:
                redirecting_link = "https://aniworld.to" + redirect_to_cache
                return redirecting_link


def vidoza_to_cache(vidoza_url):
    html_page = urllib.request.urlopen(vidoza_url)
    soup = BeautifulSoup(html_page, features="html.parser")
    for link in soup.findAll('source'):
        cache_link = str(link.get("src"))
        return(cache_link)


def test(aniworld_link):
    r = requests.get(aniworld_link, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
    print(r.url)
