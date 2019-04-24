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
        sanatized_data = {}
        for path, value in data.items():
            if len(path) > 1:
                path = "." + path
            specials = get_special_paths(path, value, {}, RedisInterface().label_to_shipper)
            if type(value) == dict:
                new_val = copy_dictionary_without_paths(value, [path_to_key_sequence(p) for p, ship_id in specials])
                for path, ship_id in specials:
                    insert_into_dictionary(new_val, path, "###Numpy_{}${}${}".format(path, time_point, ship_id))
            elif type(value).__module__ == np.__name__:
               new_val = "###Numpy_{}_{}".format(path, time_point)
            else:
                new_val = value
            sanatized_data[path] = new_val

        json_serialized = json.dumps(sanatized_data)
        return HttpResponse(json_serialized)


