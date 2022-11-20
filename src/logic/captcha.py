from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from threading import Thread


def open_captcha_window(full_url):
    options = webdriver.ChromeOptions()
    options.add_argument("app=" + full_url)
    options.add_argument("window-size=423,705")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(full_url)

    wait = WebDriverWait(driver, 100, 0.3)
    wait.until(lambda redirect: redirect.current_url != full_url)

    new_page = driver.current_url
    Thread(target=threaded_driver_close, args=(driver,)).start()
    return new_page


def threaded_driver_close(driver):
    driver.close()
