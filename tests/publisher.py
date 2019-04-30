from reem.connection import RedisInterface
from reem.datatypes import KeyValueStore

intf = RedisInterface(host="192.168.0.110")
kvs = KeyValueStore(intf)

kvs["testdata"] = "9"
print(kvs["testdata"].read())