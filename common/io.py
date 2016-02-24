import os
import datetime
import zipfile


def write_obj(file_name, obj):
    with open(file_name, 'w') as f:
        f.write(str(obj))


def write_str(file_name, s):
    with open(file_name, 'w') as f:
        f.write(s)


def write_lines(file_name, lines):
    with open(file_name, 'w') as f:
        f.writelines(lines)


def append_line(file_path, line):
    with open(file_path, "a") as f:
        f.write(line)
        f.write('\n')


def read_all(file_path):
    with open(file_path) as f:
        return f.read()


def read_all_lines(file_path):
    with open(file_path) as f:
        return f.readlines()


def read_lines(file_path, n=10):
    with open(file_path) as f:
        i = 0
        for line in f:
            i += 1
            if i <= n:
                yield line
            else:
                break


def zip_extract_all(zip_file, target_dir):
    with zipfile.ZipFile(zip_file, 'r') as z:
        z.extractall(target_dir)


def modified_on(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)


def accessed_on(filename):
    t = os.path.getatime(filename)
    return datetime.datetime.fromtimestamp(t)


def created_on(filename):
    t = os.path.getctime(filename)
    return datetime.datetime.fromtimestamp(t)

