import numpy as np
from reem.connection import RedisInterface
from reem.datatypes import KeyValueStore
import sys
import csv
import time
import os
from threading import Thread

func, keyfile, outfolder = "log", "test_key_files/key1.txt", "test_data_log/test1"
kvs = KeyValueStore(RedisInterface())


def path_to_keys(path):
    if "." in path:
        return path.split(".")
    return [path]


def log_key(key, period, key_folder):
    key_sequence = path_to_keys(key)
    next_read = time.time() + period
    while True:
        print("Entered loop")
        current = time.time()
        if current >= next_read:
            reader = kvs
            for k in key_sequence:
                reader = reader[k]
            data = reader.read()
            np.save(os.path.join(key_folder, "{}".format(int(time.time()))), data)
            print("saved")
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
            threads.append(Thread(target=log_key, args=(key, float(period), key_folder)))
            threads[-1].setDaemon(True)
            threads[-1].start()
        threads[0].join()


if __name__ == "__main__":
    log(keyfile, outfolder)