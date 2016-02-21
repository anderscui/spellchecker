import codecs


def read_all(file_name):
    with codecs.open(file_name, encoding='utf-8') as f:
        return f.read()


def read_lines(file_name, encoding='utf-8'):
    with codecs.open(file_name, encoding=encoding) as f:
        return f.readlines()


def write(file_name, s):
    with codecs.open(file_name, 'w', 'utf-8') as f:
        f.write(s)