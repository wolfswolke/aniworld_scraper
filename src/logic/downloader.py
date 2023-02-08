import time
import requests
import threading
from os import path

from zk_tools.logging_handle import logger

MODULE_LOGGER_HEAD = "downloader.py -> "


def download(link, file_name):
    downloading = True
    retry_count = 0
    while downloading:
        logger.debug(MODULE_LOGGER_HEAD + "Entered download with these vars: Link: {}, File_Name: {}".format(link, file_name))
        r = requests.get(link, stream=True)
        with open(file_name, 'wb') as f:
            for chunk in r.iter_content(1024):
                if chunk:
                    f.write(chunk)
        if retry_count == 1:
            logger.error(MODULE_LOGGER_HEAD + "Server error. Could not download {}. Please manly download it later.".format(file_name))
            downloading = False
        if path.getsize(file_name) != 0:
            downloading = False
        else:
            logger.error(MODULE_LOGGER_HEAD + "Download did not complete! File {} will be retryd in a few seconds.".format(file_name))
            logger.debug(MODULE_LOGGER_HEAD + "URL: {}, filename {}".format(link, file_name))
            time.sleep(20)
            retry_count = 1
    logger.info(MODULE_LOGGER_HEAD + "Finished download of {}.".format(file_name))


def create_new_download_thread(url, file_name):
    logger.debug(MODULE_LOGGER_HEAD + "Entered Downloader.")
    download_thread = threading.Thread(target=download, args=(url, file_name))
    download_thread.start()
    logger.info(MODULE_LOGGER_HEAD + "File {} added to queue.".format(file_name))
