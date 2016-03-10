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


def export_dict(threshold=500):
    filename = './primary_dict.txt'

    buf = []
    buf_size = 1000
    for w in en_dict:

        if en_dict[w] < threshold:
            continue

        buf.append('%s\t%d' % (w, en_dict[w]))

        if len(buf) >= buf_size:
            append_line(filename, '\n'.join(buf))
            buf = []

    if buf:
        append_line(filename, '\n'.join(buf))


def larger_than(n):
    count = 0
    for w, freq in en_dict.items():
        if freq > n:
            count += 1

    return count

if __name__ == '__main__':
    # check_dic_freq()
    # export_dict_to_file()
    # print(larger_than(387))
    print(larger_than(549))  # speling
    # print(larger_than(1000))
    # print(larger_than(10000))

    export_dict(550)
