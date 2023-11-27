import os
from threading import Thread

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait

# ------------------------------------------------------- #
#                   definitions
# ------------------------------------------------------- #
###################################################################
# Thank you @Michtdu for helping me with this Captcha Workaround. #
###################################################################

# ------------------------------------------------------- #
#                   global variables
# ------------------------------------------------------- #

# ------------------------------------------------------- #
#                      functions
# ------------------------------------------------------- #


def open_captcha_window(full_url):
    working_dir = os.getcwd()
    path_to_ublock = r'{}\extensions\ublock'.format(working_dir)
    options = webdriver.ChromeOptions()
    options.add_argument("app=" + full_url)
    options.add_argument("window-size=423,705")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    if os.path.exists(path_to_ublock):
        options.add_argument('load-extension=' + path_to_ublock)

    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(full_url)

    wait = WebDriverWait(driver, 100, 0.3)
    wait.until(lambda redirect: redirect.current_url != full_url)

    new_page = driver.current_url
    Thread(target=threaded_driver_close, args=(driver,)).start()
    return new_page


def threaded_driver_close(driver):
    driver.close()

# ------------------------------------------------------- #
#                      classes
# ------------------------------------------------------- #


# ------------------------------------------------------- #
#                       main
# ------------------------------------------------------- #
