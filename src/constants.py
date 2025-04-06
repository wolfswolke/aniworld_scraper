import sys
import re

from src.custom_logging import setup_logger

logger = setup_logger(__name__)

def check_for_old_parse():
    if sys.argv[1] == "serie" or sys.argv[1] == "anime":
        return True
    else:
        return False

use_old_parse = check_for_old_parse()

def parse_cli_arguments(default: str | int, position: int) -> str | int:
    try:
        cli_argument: str = sys.argv[position]
        logger.debug(f"cli argument detected on position:{position} with value:{cli_argument}")
        if type(default) is int:
            cli_argument: int = int(cli_argument)
        return cli_argument
    except IndexError:
        logger.debug(f"no cli argument detected on position:{position}. Using default value:{default}")
        return default

args_pattern = re.compile(
    r"("
    r"(--(?P<HELP>help).*)|"
    r"((?:-t|--type)\s(?P<TYPE>serie|anime))|"
    r"((?:-n|--name)\s(?P<NAME>[\w\-]+))|"
    r"((?:-l|--lang)\s(?P<LANG>Deutsch|Ger-Sub|English))|"
    r"((?:-m|--dl-mode)\s(?P<MODE>Series|Movies|All))|"
    r"((?:-s|--season-override)\s(?P<SEASON>\d+\+?))|"
    r"((?:-p|--provider)\s(?P<PROVIDER>VOE|Streamtape|Vidoza))"
    r")"
)

def args_parse():
    arg_line = " ".join(sys.argv[1:])
    args: dict[str, str] = {}
    if match_objects := args_pattern.finditer(arg_line):
        for match_object in match_objects:
            for item in match_object.groupdict().items():
                if item[1] != None:
                    args[item[0]] = item[1]
    return args

arguments = args_parse() if use_old_parse == False else {}

def get_arg(name: str, default: str | int = None):
    return arguments.get(name, default)

# ------------------------------------------------------- #
#                   definitions
# ------------------------------------------------------- #
APP_VERSION = "v02-10"

# ------------------------------------------------------- #
#                   global variables
# ------------------------------------------------------- #
type_of_media = parse_cli_arguments("anime", 1) if use_old_parse else get_arg("TYPE", "anime") # choose 'serie' or 'anime'
name = parse_cli_arguments("Name-Goes-Here", 2) if use_old_parse else get_arg("NAME", "Name-Goes-Here")
language = parse_cli_arguments("Deutsch", 3) if use_old_parse else get_arg("LANG", "Deutsch")
dlMode = parse_cli_arguments("Series", 4) if use_old_parse else get_arg("MODE", "Series")  # Options: Movies, Series, All
season_override = parse_cli_arguments(0, 5) if use_old_parse else get_arg("SEASON", 0)  # 0 = no override. 1 = season 1. etc...
cliProvider = parse_cli_arguments("VOE", 6) if use_old_parse else get_arg("PROVIDER", "VOE")  # 0 = no override. 1 = season 1. etc...
episode_override = 0  # 0 = no override. 1 = episode 1. etc...
ddos_protection_calc = 5
ddos_wait_timer = 60  # in seconds
max_download_threads = 5 # This does NOT limit the threads but won't start more when the DDOS Timer starts.
thread_download_wait_timer = 30  # in seconds
disable_thread_timer = False # If true the script will start downloads as soon as the ddos protection is over.
output_root = "output"
output_name = name
output_path = f"{output_root}/{type_of_media}/{output_name}"
site_url = {
    "serie": "https://s.to",  # maybe you need another dns to be able to use this site
    "anime": "https://aniworld.to"
}
provider_priority = ["VOE", "Vidoza", "Streamtape"]

url = "{}/{}/stream/{}/".format(site_url[type_of_media], type_of_media, name)

