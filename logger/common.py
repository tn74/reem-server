import numpy as np
import os


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


def retrieve_data_at_time(log_folder, time):
    """
    Analyze log data for information at a specific time
    :param log_folder: Absolute path (to make things easy) of log's data folder
    :param time: Time at which to extract information
    :return:
    """
    data = {}
    for path_name in os.listdir(log_folder):
        key_dir = os.path.join(log_folder, path_name)
        timestamps = sorted([float(record.replace("_", ".")[:-4]) for record in os.listdir(key_dir)])
        timestamp_index = binary_search(timestamps, 0, len(timestamps)-1, time)
        if timestamp_index is None:
            continue
        desired_timestamp = timestamps[timestamp_index]
        desired_record_name = os.path.join(key_dir, "{}".format(desired_timestamp).replace(".", "_") + ".npy")
        value = np.load(desired_record_name)
        data[path_name] = value
        if value.dtype == np.object:
            data[path_name] = value.item()
        if np.isscalar(data[path_name]):
            data[path_name] = float(data[path_name])
    return data
