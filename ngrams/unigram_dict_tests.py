from common.io import append_line
from common.persistence import from_pickle

en_dict = from_pickle('../data/ngrams/en_dict.pkl')


def check_dic_freq():
    print(en_dict['the'])
    print(en_dict['of'])
    print(en_dict['and'])
    print(en_dict['to'])
    print(en_dict['a'])
    print(en_dict['in'])
    print(en_dict['for'])
    print
    print(en_dict['click'])

    print(en_dict["doesn't"])
    print(en_dict["can't"])
    print(en_dict["cannot"])

    print(en_dict["first-class"])

    # non-real words
    print
    print(en_dict['good'])
    print(en_dict['goood'])
    print(en_dict['spelling'])
    print(en_dict['speling'])


def export_dict_to_file():
    filename = './dict.txt'

    buf = []
    buf_size = 1000
    for w in en_dict:
        buf.append('%s\t%d' % (w, en_dict[w]))

        if len(buf) >= buf_size:
            append_line(filename, '\n'.join(buf))
            buf = []

    if buf:
        append_line(filename, '\n'.join(buf))


if __name__ == '__main__':
    # check_dic_freq()
    export_dict_to_file()
