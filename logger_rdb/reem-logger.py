import os
from shutil import copyfile
import time
import redis
import sys


def log(out_folder, dump_rdb_path, period):
    client = redis.Redis()
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)

    while True:
        current_time = str(int(time.time() * 1000))
        copyfile(dump_rdb_path, os.path.join(out_folder, "{}millis.rdb".format(current_time)))
        client.bgsave()
        time.sleep(period)


if __name__ == "__main__":
    out_folder = "test_data_rdb/test1"
    dump_rdb_path = "../dump.rdb"
    period = 2
    if len(sys.argv) == 4:
        _, out_folder, dump_rdb_path, period = sys.argv
    if len(sys.argv) == 3:
        _, out_folder, dump_rdb_path = sys.argv
    if len(sys.argv) == 2:
        _, out_folder = sys.argv[0]
    period = float(period)

    print("Saving to:   {} \nSaving from: {}\nPeriod = {} s".format(out_folder, dump_rdb_path, period))
    log(out_folder, dump_rdb_path, period)