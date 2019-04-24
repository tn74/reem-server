from django.shortcuts import render, reverse
from django.views import View
from django.http import HttpResponse
from django.conf import settings
from reem.connection import RedisInterface
from reem.datatypes import KeyValueStore
import numpy as np
import scipy
import time
import json
import os
from reem.helper_functions import *
from reem.connection import RedisInterface
# Create your views here.
from logger import common


class Retrieval(View):
    def get(self, request, log_folder, time_point):
        log_folder = log_folder.replace("$", "/")
        data = common.retrieve_data_at_time(os.path.join(os.getcwd(), "logger", log_folder), float(time_point))
        print(data)
        for path, v in data.items():
            json_incompatible_paths = {}
            if len(path) > 1:
                p = "." + path
            else:
                p = path
            print(p)
            print(get_special_paths(p, v, json_incompatible_paths, RedisInterface().label_to_shipper))
            print(json_incompatible_paths)
            print(type(v))
            if type(v) == dict:
                new_val = copy_dictionary_without_paths(v, [path_to_key_sequence(p) for p in json_incompatible_paths.keys()])
                for path in json_incompatible_paths:
                    insert_into_dictionary(new_val, path, "###Numpy_{}_{}".format(path, time_point))
                data[path] = new_val
            elif type(v).__module__ == np.__name__:
                data[path] = "###Numpy_{}_{}".format(path, time_point)

        json_serialized = json.dumps(data)
        return HttpResponse(json_serialized)


