from bs4 import BeautifulSoup

from src.custom_logging import setup_logger

logger = setup_logger(__name__)


class ProviderError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class LanguageError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

language_mapping = ["Deutsch", "Ger-Sub", "English"]

def restructure_dict(given_dict):
    new_dict = {}
    already_seen = set()
    for key, value in given_dict.items():
        new_dict[value] = set([element.strip() for element in key.split(',')])
    return_dict = {}
    for key, values in new_dict.items():
        for value in values:
            if value in already_seen and value in return_dict:
                del return_dict[value]
                continue
            if value not in already_seen and value not in return_dict:
                return_dict[value] = key
                already_seen.add(value)
    return return_dict


def extract_lang_key_mapping(soup):
    lang_key_mapping = {}
    # Find the div with class "changeLanguageBox"
    change_language_div = soup.find("div", class_="changeLanguageBox")
    if change_language_div:
        # Find all img tags inside the div to extract language and data-lang-key
        lang_elements = change_language_div.find_all("img")
        for lang_element in lang_elements:
            language = lang_element.get("alt", "") + "," + lang_element.get("title", "")
            data_lang_key = lang_element.get("data-lang-key", "")
            if language and data_lang_key:
                lang_key_mapping[language] = data_lang_key
    ret = restructure_dict(lang_key_mapping)
    logger.debug(f"Restructured language mapping: {ret}")
    return ret


def get_href_by_language(html_content, language, provider):
    soup = BeautifulSoup(html_content, "html.parser")
    lang_key_mapping = extract_lang_key_mapping(soup)
    lang_key_mapping = {k: v for k, v in lang_key_mapping.items() if k in language_mapping}

    if not lang_key_mapping:
        raise LanguageError(logger.error("No language mapping found."))

    # Debug logs
    logger.debug(f"Language mapping: {lang_key_mapping}")
    logger.debug(f"Given language: {language}")

    # Find the data-lang-key value based on the input language
    lang_key = lang_key_mapping.get(language)
    if lang_key is None:
        logger.error(f"Invalid language input. Supported languages: {list(lang_key_mapping.keys())}")
        logger.warning(f"Using first language in mapping: {list(lang_key_mapping.keys())[0]}")
        lang_key = list(lang_key_mapping.values())[0]
        used_lang = list(lang_key_mapping.keys())[0]
    else:
        used_lang = language
    # Find all <li> elements with the given data-lang-key value and h4=provider"
    matching_li_elements = soup.find_all("li", {"data-lang-key": lang_key})
    matching_li_element = next((li_element for li_element in matching_li_elements
                                if li_element.find("h4").get_text() == provider), None)
    # Check if any matching elements were found and return the corresponding href
    if matching_li_element:
        href = matching_li_element.get("data-link-target", "")
        return href, used_lang
    raise ProviderError(logger.error(f"No matching download found for language '{language}' and provider '{provider}'"))
