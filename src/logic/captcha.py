"""

"""
# ------------------------------------------------------- #
#                     imports
# ------------------------------------------------------- #
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from threading import Thread

import os

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
    # if you encounter this error ___selenium.common.exceptions.WebDriverException: Message: unknown error: cannot find Chrome binary____
    # set the next line to the specific Google Chrome binary on your system
    # options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
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
