
def write_obj(file_name, obj):
    with open(file_name, 'w') as f:
        f.write(str(obj))


def write_str(file_name, s):
    with open(file_name, 'w') as f:
        f.write(s)


def write_line(f, s):
    if isinstance(s, basestring):
        f.write(s)
    else:
        f.write(str(s))
    f.write('\n')


def write_lines(file_name, lines):
    with open(file_name, 'w') as f:
        f.writelines(lines)


def read_all(file_name):
    with open(file_name) as f:
        return f.read()


def read_lines(file_name):
    with open(file_name) as f:
        return f.readlines()


import os
import datetime


def modified_on(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)


def accessed_on(filename):
    t = os.path.getatime(filename)
    return datetime.datetime.fromtimestamp(t)


def created_on(filename):
    t = os.path.getctime(filename)
    return datetime.datetime.fromtimestamp(t)