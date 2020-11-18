import json
import pickle
import os
from abc import ABCMeta, abstractmethod



class ParamHandler(metaclass=ABCMeta):
    def __init__(self, source):
        self.source = source
        self.params = {}

    def add_param(self, key, value):
        self.params[key] = value

    def get_param(self, key):
        return self.params.get(key)

    def get_all_params(self):
        return self.params

    def remove_param(self,key):
        del self.params[key]

    def remove_all_params(self):
        self.params.clear()

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self):
        pass



class JsonParamHandler(ParamHandler):
    def read(self):
        """Чтение из json файла и присвоение значений в self.params"""
        with open(self.source, 'r') as f:
            read_json_params = json.load(f)
            self.params.update(read_json_params)

    def write(self):
        """Запись в json файл параметров self.params"""
        with open(self.source, 'w') as f:
            json.dump(self.params, f)


class PickleParamHandler(ParamHandler):
    def read(self):
        """Чтение в формате pickle и присвоение значений в self.params"""
        with open(self.source, 'rb') as f:
            read_pickle_params = pickle.load(f)
            self.params.update(read_pickle_params)

    def write(self):
        """Запись в формате pickle параметров self.params"""
        with open(self.source, 'wb') as f:
            pickle.dump(self.params,f)


class ParamHandlerException(Exception):
    pass

class ParamHandlerFactory(object):
    types = {}

    @classmethod
    def add_type(cls, name, klass):
        if not name:
            raise ParamHandlerException('Type must have a name.')

        if not issubclass(klass, ParamHandler):
            raise ParamHandlerException(
                'Class "{}" is not ParamHandler.'.format(klass)
            )
        cls.types[name] = klass

    @classmethod
    def create(cls, source):
        _, ext = os.path.splitext(str(source).lower())
        ext = ext.lstrip('.')
        klass = cls.types.get(ext)
        if klass is None:
            raise ParamHandlerException(
                'Type "{}" not found.'.format(ext)
            )
        return klass(source)

ParamHandlerFactory.add_type('json', JsonParamHandler)
ParamHandlerFactory.add_type('pickle', PickleParamHandler)
