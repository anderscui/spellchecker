import glob
import os
import re

import datetime
from collections import defaultdict

from common.io import append_line
from common.persistence import to_pickle

re_en_word = re.compile(r"^[a-z-'.]+$")


def is_english_word(w):
    return re_en_word.match(w) is not None


def read_word_freq(line):
    parts = line.split('\t')
    if is_english_word(parts[0]):
        return parts[0].lower(), int(parts[1])
    else:
        return None, None


def build_unigram_dict(data_dir):

    cwd = os.getcwdu()
    print('cwd: {0}'.format(cwd))
    print('change wd to: {0}'.format(data_dir))
    os.chdir(data_dir)

    output_dir = './1gram/'
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    en_dict = defaultdict(int)
    line_counter = 0
    word_counter = 0

    for data_file in glob.glob('*1gram-20090715*.txt'):
        print('extracting data from: ' + data_file)

        with open(data_file) as f:
            for raw_line in f:
                line_counter += 1
                word, freq = read_word_freq(raw_line)
                if word is not None:
                    word_counter += 1
                    en_dict[word] += freq

    to_pickle(en_dict, './1gram/en_dict.pkl')
    print('total lines: {}'.format(line_counter))
    print('total word lines: {}'.format(word_counter))
    print('total unique words: {}'.format(len(en_dict)))

    print('change wd back to: {0}'.format(cwd))
    os.chdir(cwd)


if __name__ == '__main__':
    build_unigram_dict(r'D:\andersc\downloads\googlebooks-eng-1M-ngrams\ngrams\token-freq')
