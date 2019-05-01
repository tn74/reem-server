from reem.connection import RedisInterface
from reem.datatypes import KeyValueStore
from scipy.misc import imread
import os

intf = RedisInterface()
intf.initialize()

kvs = KeyValueStore(intf)
image_fname = os.path.join(os.path.dirname(os.path.abspath(__file__)), "redis_image.png")
kvs["image_dict"] = {"image": imread(image_fname)}
