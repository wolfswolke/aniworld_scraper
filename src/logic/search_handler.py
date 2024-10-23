import requests
from thefuzz import process
from bs4 import BeautifulSoup

class Search_Handler:
    def __init__(self):
        self.base_url = f"https://aniworld.to/animes"
        self.base_url_sto = f"https://s.to/serien"
        self.anime_names = []
        self.show_names = []


    def get_hosted_media_names(self, media_hoster: str):
        if media_hoster == "aniworld":
            url = self.base_url
        elif media_hoster == "sto":
            url = self.base_url_sto
        else:
            return None
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        name_list = []
        for name in soup.find_all('div', class_='genre'):
            for a in name.find_all('a'):
                text = a.get_text()
                href = a.get('href')
                alt_tags = a.get('data-alternative-title')
                alt_tag_list = []
                for alt_tag in alt_tags.split(", "):
                    if alt_tag:
                        name_list.append([href, alt_tag])
                name_list.append([href, text])
        return name_list
    # ('Wettlauf zum Mittelpunkt der Erde', '/serie/stream/wettlauf-zum-mittelpunkt-der-erde', ['Course au Centre de la Terre', 'Race to the Centre of the Earth'])

    def search_by_name(self, name, hoster):
        if hoster == "aniworld":
            name_list = self.anime_names
        elif hoster == "sto":
            name_list = self.show_names
        else:
            return None
        if not name_list:
            name_list = self.get_hosted_media_names(hoster)
        ret = process.extractBests(name, name_list, limit=10)
        return ret


search_handler = Search_Handler()

if __name__ == "__main__":
    # name_list = search_handler.search_by_name("Naruto", "aniworld")
    name = input("Enter the name of the show: ")
    if not name:
        print("No name entered")
        exit(1)
    name_list = search_handler.search_by_name(name, "aniworld")
    choice_list = []
    choice_id = 0
    if name_list:
        print("Please slect from the results below:")
        print("")
        for name in name_list:
            print(f"{choice_id} - Name: {name[0][1]}, URL: {name[0][0]}")
            choice_list.append([choice_id, name[0][0]])
            choice_id += 1
    else:
        print("No results found")
        exit(2)
    choice = input("Enter the number of the show you want to watch: ")
    if not choice:
        print("No choice entered")
        exit(3)
    choice = int(choice)
    if choice < 0 or choice > choice_id:
        print("Invalid choice")
        exit(4)
    try:
        print(f"Selected: {choice_list[choice][1]}")
        print("Done")
    except IndexError:
        print("Invalid choice")
        exit(5)

