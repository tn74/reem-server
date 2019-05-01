import os
from rdbtools import RdbParser, JSONCallback


def binary_search(arr, l, r, val):
    if r - l <= 1:
        if arr[l] <= val <= arr[r]:
            return l
        else:
            return None
    m = int((r + l)/2)
    if arr[m] <= val:
        return binary_search(arr, m, r, val)
    else:
        return binary_search(arr, l, m, val)


def get_rdb_file(log_folder, time):
    timestamps = sorted([float(record.split("millis")[0]) for record in os.listdir(log_folder)])
    timestamp_index = binary_search(timestamps, 0, len(timestamps)-1, time)
    desired_timestamp = timestamps[timestamp_index]
    return os.path.join(log_folder, "{}millis.rdb".format(int(desired_timestamp)))


def retrieve_data_at_time(log_folder, time):
    """
    Analyze log data for information at a specific time
    :param log_folder: Absolute path (to make things easy) of log's data folder
    :param time: Time at which to extract information
    :return:
    """
    rdb_fpath = get_rdb_file(log_folder, time)
    parser = RdbParser(JSONCallback(open("ss", "wb")))
    return parser.parse(rdb_fpath)


if __name__ == "__main__":
    log_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_data_rdb/test1/")
    print(retrieve_data_at_time(log_folder, 1556668273471))
