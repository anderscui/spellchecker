import glob
import os

from collections import defaultdict

from common.persistence import to_pickle
from ngrams import is_english_word


def read_word_freq(line):
    parts = line.split('\t')
    return parts[0], int(parts[1])


def build_unigram_dict(data_dir):

    cwd = os.getcwdu()
    print('cwd: {0}'.format(cwd))
    print('change wd to: {0}'.format(data_dir))
    os.chdir(data_dir)

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

    to_pickle(en_dict, './en_dict.pkl')
    print('total lines: {}'.format(line_counter))
    print('total word lines: {}'.format(word_counter))
    print('total unique words: {}'.format(len(en_dict)))

    print('change wd back to: {0}'.format(cwd))
    os.chdir(cwd)


# dict stats
# Min.   :1.000e+00
# 1st Qu.:3.900e+01
# Median :1.090e+02
# Mean   :2.960e+04
# 3rd Qu.:3.870e+02
# Max.   :4.212e+09
if __name__ == '__main__':
    build_unigram_dict(r'/Users/andersc/data/googlebooks-eng-1M-ngrams/1gram/token-freq/1gram/')
