import sys

def parse_cli_arguments(default: str | int, position: int) -> str | int:
    try:
        cli_argument: str = sys.argv[position]
        if type(default) is int:
            cli_argument: int = int(cli_argument)
        return cli_argument
    except IndexError:
        return default

type_of_media = parse_cli_arguments("anime", 1)  # choose 'serie' or 'anime'
name = parse_cli_arguments("Name-Goes-Here", 2)
site_url = {
    "serie": "https://s.to",  # maybe you need another dns to be able to use this site
    "anime": "https://aniworld.to"
}
url = "{}/{}/stream/{}/".format(site_url[type_of_media], type_of_media, name)