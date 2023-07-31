import time
import requests
import threading
import subprocess
import platform
import os

from os import path
from zk_tools.logging_handle import logger

MODULE_LOGGER_HEAD = "downloader.py -> "


def already_downloaded(file_name):
    if os.path.exists(file_name) and os.path.getsize(file_name) > 0:
        logger.info(MODULE_LOGGER_HEAD + "Episode {} already downloaded.".format(file_name))
        return True
    logger.debug(MODULE_LOGGER_HEAD + "File not downloaded. Downloading: {}".format(file_name))
    return False


def download(link, file_name):
    retry_count = 0
    while True:
        logger.debug(MODULE_LOGGER_HEAD + "Entered download with these vars: Link: {}, File_Name: {}".format(link, file_name))
        r = requests.get(link, stream=True)
        with open(file_name, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
        if path.getsize(file_name) != 0:
            logger.info(MODULE_LOGGER_HEAD + "Finished download of {}.".format(file_name))
            break
        elif retry_count == 1:
            logger.error(MODULE_LOGGER_HEAD + "Server error. Could not download {}. Please manly download it later.".format(file_name))
            break
        else:
            logger.info(MODULE_LOGGER_HEAD + "Download did not complete! File {} will be retryd in a few seconds.".format(file_name))
            logger.debug(MODULE_LOGGER_HEAD + "URL: {}, filename {}".format(link, file_name))
            time.sleep(20)
            retry_count = 1
        

def download_and_convert_hls_stream(hls_url, file_name):
    try:
        ffmpeg_cmd = ['ffmpeg', '-i', hls_url, '-c', 'copy', file_name]
        if platform.system() == "Windows":
            subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)    
        logger.info(MODULE_LOGGER_HEAD + "Finished download of {}.".format(file_name))
    except subprocess.CalledProcessError as e:
        logger.error(MODULE_LOGGER_HEAD + "Server error. Could not download {}. Please manly download it later.".format(file_name))


def create_new_download_thread(url, file_name, provider):
    logger.debug(MODULE_LOGGER_HEAD + "Entered Downloader.")
    if provider == "Vidoza":
        download_thread = threading.Thread(target=download, args=(url, file_name))
        download_thread.start()
    elif provider == "VOE":
        download_thread = threading.Thread(target=download_and_convert_hls_stream, args=(url, file_name))
        download_thread.start()
    logger.info(MODULE_LOGGER_HEAD + "File {} added to queue.".format(file_name))
