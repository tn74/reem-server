import numpy as np
from reem.connection import RedisInterface
from reem.datatypes import KeyValueStore
import sys
import csv
import time
import os
from threading import Thread
import logging

FORMAT = "%(threadName)10s %(asctime)20s %(filename)30s:%(lineno)3s  %(funcName)20s() %(levelname)10s     %(message)s"
logging.basicConfig(format=FORMAT)

logger = logging.getLogger("reem.datatypes")
logger.setLevel(logging.DEBUG)

func, keyfile, outfolder = "log", "test_key_files/key1.txt", "test_data_log/test1"
kvs = KeyValueStore(RedisInterface())


def path_to_keys(path):
    if "." in path:
        return path.split(".")
    return [path]


def log_path(path, period, key_folder):
    key_sequence = path_to_keys(path)
    next_read = time.time() + period
    while True:
        logger.debug("Path       : {}".format(path))
        current = time.time()
        if current >= next_read:
            # print("{} Current >= next_read".format(path))
            reader = kvs
            for k in key_sequence:
                reader = reader[k]
            logger.debug("PathHandler: {} {}".format(reader.reader.top_key_name, reader.path))
            data = reader.read()
            np.save(os.path.join(key_folder, "{}".format(current).replace(".", "_")), data)  # . in time replaced with _
            next_read = current + period
        else:
            time.sleep(next_read - time.time())


def log(key_fpath, out_path):
    with open(key_fpath, "r") as f:
        threads = []
        reader = csv.reader(f)
        for key, period in reader:
            key_folder = os.path.join(out_path, key)
            if not os.path.exists(key_folder):
                os.makedirs(key_folder)
            threads.append(Thread(target=log_path, args=(key, float(period), key_folder)))
            threads[-1].setDaemon(True)
            threads[-1].start()
        threads[0].join()


if __name__ == "__main__":
    log(keyfile, outfolder)