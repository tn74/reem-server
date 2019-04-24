from django.shortcuts import render, reverse
from django.views import View
from django.http import HttpResponse
from django.conf import settings
from reem.connection import RedisInterface
from reem.datatypes import KeyValueStore
import numpy as np
import scipy
import time
# Create your views here.


def get_content(path):
    try:
        keys = [path]
        if "." in path:
            keys = path.split(".")
        pfinder = kvs
        for k in keys:
            pfinder = pfinder[k]
        val = pfinder.read()
        print(val)
    except Exception:
        val = "Could not find entry matching {}".format(path)
    return val


class ContentView(View):
    def get(self, request, path):
        content = get_content(path)
        html = self.html_content(request, content, path)
        return render(request, "view.html", {"display_html": html, "search":path})

    def html_content(self, request, content, path, depth=0):
        html_full = "<div class=\"container\">\n {} \n</div>"
        if type(content) is not dict:
            formatted_data = self.process_terminal_value(request, content, path, depth)
            return html_full.format(formatted_data)

        formatted_data = ""
        for k, v in content.items():
            if type(v) is dict:
                drop_down_id = "depth{}_key{}".format(depth, k)
                key_string = "<a data-toggle=\"collapse\" href=\"#{}\"><p> {}</p></a>"\
                    .format(drop_down_id, k)
                internal_div = "{}\n<div class=\"collapse\" id={}>\n {} \n</div>"\
                    .format(key_string, drop_down_id, self.html_content(request, v, path + "." + k, depth+1))
                formatted_data += internal_div
            else:
                formatted_data += self.process_terminal_value(request, v, path + "." + k, depth)

        return html_full.format(formatted_data)

    def process_terminal_value(self, request, value, path, depth):
        key = path
        if "." in key:
            key = key.split(".")[-1]
        padded_key_string = "{}".format(key)
        padded_key_string += "".join(["&nbsp;" for i in range(20 - len(padded_key_string))])
        indents = "".join("&nbsp;" for i in range(depth * 2))
        if type(value).__module__ == np.__name__:
            np_key_link = "http://{}{}".format(request.META['HTTP_HOST'], reverse('browser_app:npview', kwargs={'path': path}))
            print(np_key_link)
            value = "<a href=\"{}\">np_array_list_view</a>" \
                .format(np_key_link)
        formatted_data = "<p>{}{}{}</p>".format(indents, padded_key_string, value)
        return formatted_data


class NumpyView(View):
    def get(self, request, path):
        arr = get_content(path)
        if not type(arr).__module__ == np.__name__:
            return render(request, "view.html", {"display_html": "No Numpy Array Here", "search": path})
        else:
            return render(request, "view.html", {"display_html": self.make_numpy_string(arr), "search": path})

    def make_numpy_string(self, arr, depth=0):
        indents = "".join(["&nbsp;" for i in range(depth * 3)])
        ret_string = "<p>{}[</p>".format(indents)
        for val in arr:
            if np.isscalar(val):
                ret_string += "<p>{}&nbsp;{}</p>".format(indents, val)
            else:
                ret_string += self.make_numpy_string(val, depth+1)
        ret_string += "<p>{}]</p>".format(indents)
        return ret_string


class NumpyImageView(View):
    def get(self, request, path):
        arr = get_content(path)
        if not type(arr).__module__ == np.__name__:
            return render(request, "view.html", {"display_html": "No Numpy Array Here", "search": path})
        else:
            return render(request, "view.html", {"display_html": self.display_np_image(arr), "search": path})

    def display_np_image(self, arr, depth=0):
        fname = "{}.jpg".format(int(time.time()))
        scipy.misc.toimage(arr, cmin=0.0, cmax=255).save("browswer_app/static/{}".format(fname))
        return "<img src=\"{% static '{}' %}\" / >".format(fname)


class Home(View):
    def get(self, request):
        return render(request, "welcome_page.html")