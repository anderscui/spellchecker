import codecs
import pickle
import json


def to_pickle(obj, file_path, protocol=pickle.HIGHEST_PROTOCOL):
    with open(file_path, 'wb') as output:
        pickle.dump(obj, output, protocol)


def from_pickle(file_path):
    with open(file_path, 'rb') as data_file:
        return pickle.load(data_file)


def to_json(obj, file_path):
    # with codecs.open(file_path, 'w', 'utf-8') as output:
    with open(file_path, 'w') as output:
        json.dump(obj, output)


def from_json(file_path):
    with open(file_path) as json_file:
        return json.load(json_file)

