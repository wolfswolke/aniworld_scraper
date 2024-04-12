import os
import platform
import subprocess
import time
from os import path
from threading import Thread

import requests

from src.custom_logging import setup_logger
from src.failures import append_failure, remove_file
from src.successes import append_success

logger = setup_logger(__name__)


def already_downloaded(file_name):
    if os.path.exists(file_name) and os.path.getsize(file_name) > 0:
        logger.info("Episode {} already downloaded.".format(file_name))
        return True
    logger.debug("File not downloaded. Downloading: {}".format(file_name))
    return False


def download(link, file_name):
    retry_count = 0
    while True:
        logger.debug("Entered download with these vars: Link: {}, File_Name: {}".format(link, file_name))
        r = requests.get(link, stream=True)
        with open(file_name, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
        if path.getsize(file_name) != 0:
            logger.success("Finished download of {}.".format(file_name))
            append_success(file_name)
            break
        elif retry_count == 1:
            logger.error("Server error. Could not download {}. Please manly download it later.".format(file_name))
            append_failure(file_name)
            remove_file(file_name)
            break
        else:
            logger.info("Download did not complete! File {} will be retryd in a few seconds.".format(file_name))
            logger.debug("URL: {}, filename {}".format(link, file_name))
            time.sleep(20)
            retry_count = 1


def download_and_convert_hls_stream(hls_url, file_name):
    if path.exists("ffmpeg.exe"):
        ffmpeg_path = "ffmpeg.exe"
    elif path.exists("src/ffmpeg.exe"):
        ffmpeg_path = "src/ffmpeg.exe"
    else:
        ffmpeg_path = "ffmpeg"

    try:
        ffmpeg_cmd = [ffmpeg_path, '-i', hls_url, '-c', 'copy', file_name]
        if platform.system() == "Windows":
            subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        logger.success("Finished download of {}.".format(file_name))
        append_success(file_name)
    except subprocess.CalledProcessError as e:
        logger.error("Server error. Could not download {}. Please manly download it later.".format(file_name))
        append_failure(file_name)
        remove_file(file_name)


def create_new_download_thread(url, file_name, provider) -> Thread:
    logger.debug("Entered Downloader.")
    t = None
    if provider in ["Vidoza", "Streamtape"]:
        t = Thread(target=download, args=(url, file_name))
        t.start()
    elif provider == "VOE":
        t = Thread(target=download_and_convert_hls_stream, args=(url, file_name))
        t.start()
    logger.loading("Provider {} - File {} added to queue.".format(provider, file_name))
    return t
