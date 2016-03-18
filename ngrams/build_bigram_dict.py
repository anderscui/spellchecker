import glob
import os

from collections import defaultdict

import datetime

from common.io import append_line
from common.persistence import to_pickle


def read_ngram_freq(line):
    parts = line.split('\t')
    return parts[0], int(parts[1])


def build_bigram_dict(data_dir):

    cwd = os.getcwdu()
    print('cwd: {0}'.format(cwd))
    print('change wd to: {0}'.format(data_dir))
    os.chdir(data_dir)

    en_dict = defaultdict(int)
    line_counter = 0
    word_counter = 0

    for data_file in glob.glob('*2gram-20090715*.txt'):
        print('extracting data from: ' + data_file)

        with open(data_file) as f:
            for line in f:
                line_counter += 1
                word, freq = read_ngram_freq(line)
                if word is not None:
                    word_counter += 1
                    en_dict[word] += freq

        print('extracting data from {} done'.format(data_file))

    # to_pickle(en_dict, './en_bigram.pkl')

    # write ngram+freq
    print(datetime.datetime.now())
    output_file = './bigram_dict_less.txt'
    buf = []
    buf_size = 1000
    threshold = 227
    for gram in en_dict:
        gram_freq = en_dict[gram]
        if gram_freq < threshold:
            continue

        buf.append('%s\t%d' % (gram, gram_freq))
        if len(buf) >= buf_size:
            append_line(output_file, '\n'.join(buf))
            buf = []
    if buf:
        append_line(output_file, '\n'.join(buf))
    print(datetime.datetime.now())

    # # write freq only
    # print(datetime.datetime.now())
    # output_file = './bigram_freq.txt'
    # buf = []
    # buf_size = 1000
    # for gram in en_dict:
    #     buf.append(str(en_dict[gram]))
    #     if len(buf) >= buf_size:
    #         append_line(output_file, '\n'.join(buf))
    #         buf = []
    # if buf:
    #     append_line(output_file, '\n'.join(buf))
    # print(datetime.datetime.now())

    print('total lines: {}'.format(line_counter))
    print('total word lines: {}'.format(word_counter))
    print('total unique words: {}'.format(len(en_dict)))

    print('change wd back to: {0}'.format(cwd))
    os.chdir(cwd)


def build_trigram_dict(data_dir):

    cwd = os.getcwdu()
    print('cwd: {0}'.format(cwd))
    print('change wd to: {0}'.format(data_dir))
    os.chdir(data_dir)

    en_dict = defaultdict(int)
    line_counter = 0
    word_counter = 0
    threshold = 100

    for data_file in glob.glob('*3gram-20090715*.txt'):
        print('extracting data from: ' + data_file)

        with open(data_file) as f:
            for line in f:
                line_counter += 1
                word, freq = read_ngram_freq(line)
                if word is not None:
                    word_counter += 1
                    if freq > threshold:
                        en_dict[word] += freq

        print('extracting data from {} done'.format(data_file))

    # to_pickle(en_dict, './en_bigram.pkl')

    # write ngram+freq
    print(datetime.datetime.now())
    output_file = './trigram_dict.txt'
    buf = []
    buf_size = 1000
    # threshold = 100
    for gram in en_dict:
        gram_freq = en_dict[gram]
        if gram_freq < threshold:
            continue

        buf.append('%s\t%d' % (gram, gram_freq))
        if len(buf) >= buf_size:
            append_line(output_file, '\n'.join(buf))
            buf = []
    if buf:
        append_line(output_file, '\n'.join(buf))
    print(datetime.datetime.now())

    # # write freq only
    # print(datetime.datetime.now())
    # output_file = './trigram_freq.txt'
    # buf = []
    # buf_size = 1000
    # for gram in en_dict:
    #     buf.append(str(en_dict[gram]))
    #     if len(buf) >= buf_size:
    #         append_line(output_file, '\n'.join(buf))
    #         buf = []
    # if buf:
    #     append_line(output_file, '\n'.join(buf))
    # print(datetime.datetime.now())

    print('total lines: {}'.format(line_counter))
    print('total word lines: {}'.format(word_counter))
    print('total unique words: {}'.format(len(en_dict)))

    print('change wd back to: {0}'.format(cwd))
    os.chdir(cwd)


# dict stats
# total word lines: 37917840
# total unique words: 31480919
# Min.   :        1
# 1st Qu.:       42
# Median :       83
# Mean   :     1685
# 3rd Qu.:      227
# Max.   :685937530
if __name__ == '__main__':
    # build_bigram_dict(r'/Users/andersc/data/eng-1M-ngrams-tokens/2gram-tokens/2gram/')
    # 200
    # total lines: 117155205
    # total word lines: 117155205
    # total unique words: 17965450

    # 100
    # total unique words: 33559929

    # 50
    # total unique words: 61041399
    build_trigram_dict(r'D:\andersc\downloads\googlebooks-eng-1M-ngrams\3gram\token-freq\3gram')
