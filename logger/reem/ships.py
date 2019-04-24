from abc import ABC, abstractmethod
import numpy as np
import io


class SpecialCaseShip(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def check_fit(self, value):
        """
        Check if the value is such that this is the class that ought to handle storing and loading it
        :param value:
        :return:
        """
        pass

    @abstractmethod
    def write(self, key, value, client):
        """
        Given a top level key name and a value, write to the redis database however you choose
        :param key: Top Key to store value under in redis
        :param value: Data to store
        :param client: Client to use
        :return: None
        """
        pass

    @abstractmethod
    def read(self, key, client):
        """
        Issue ONE ACTION you need to retrieve information from redis
        :param key: Top Key under which the encoded value is stored
        :param client: Client to use
        :return: None
        """
        pass

    @abstractmethod
    def interpret_read(self, responses):
        """
        Your client actions in the read method returned a series of responses from redis.
        This method interprets them and gives the result
        :param responses: responses from Redis Client
        :return: Value of object when read
        """
        pass

    @abstractmethod
    def get_label(self):
        """
        Return a string that will be used in key names to indicate this class should be used to decode data
        """
        pass


class NumpyShip(SpecialCaseShip):
    def check_fit(self, value):
        return type(value) in [np.array, np.ndarray]

    def write(self, key, value, client):
        client.hset(key, "arr", bytes(memoryview(value.data)))
        client.hset(key, "dtype", str(value.dtype))
        client.hset(key, "shape", str(value.shape))
        client.hset(key, "strides", str(value.strides))

    def get_label(self):
        return "default_numpy_handler"

    def read(self, key,  client):
        client.hgetall(key)

    def interpret_read(self, responses):
        hash = responses[0]
        dtype = eval("np.{}".format(hash[b'dtype'].decode('utf-8')))
        shape = hash[b'shape'].decode("utf-8")[1:-1]
        shape = tuple([int(s) for s in shape.split(",") if len(s) > 0])
        arr = np.frombuffer(hash[b'arr'], dtype)
        arr = np.reshape(arr, shape)
        return arr
