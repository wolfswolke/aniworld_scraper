from tqdm import tqdm
import requests
import threading

from gutils.logging_handle import logger

MODULE_LOGGER_HEAD = "downloader.py -> "


def download(link, file_name):
    logger.debug(MODULE_LOGGER_HEAD + "Entered download with these vars: Link: {}, File_Name: {}".format(link, file_name))
    r = requests.get(link, stream=True)
    with open(file_name, 'wb') as f:
        for chunk in r.iter_content(1024):
            if chunk:
                f.write(chunk)
    logger.info(MODULE_LOGGER_HEAD + "Finished download of {}.".format(file_name))


def create_new_download_thread(url, file_name):
    logger.debug(MODULE_LOGGER_HEAD + "Entered Downloader.")
    download_thread = threading.Thread(target=download, args=(url,file_name))
    download_thread.start()
    logger.info(MODULE_LOGGER_HEAD + "File {} added to queue.".format(file_name))


def downloader(url, file_name):
    # Old Downloader.
    response = requests.get(url, stream=True, timeout=10)
    total_size_in_bytes = int(response.headers.get('content-length', 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    with open(file_name, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("ERROR, something went wrong")
