import glob
import os
import re

import datetime

from common.io import append_line

re_en_word = re.compile(r"^[a-z-'.]+$")


def is_english_word(w):
    return re_en_word.match(w) is not None


def read_word_freq(line):
    parts = line.split('\t')
    if is_english_word(parts[0]):
        return parts[0].lower(), int(parts[1])
    else:
        return None, None


def build_unigram(data_file, output_file):
    """
    extract token stats in the data_file, save it in output_file.
    :param data_file:
    :param output_file:
    """
    start_time = datetime.datetime.now()
    # print(start_time)
    print('extracting started...')

    with open(data_file) as f:

        line_counter = 0
        word_counter = 0

        for raw_line in f:

            word, freq = read_word_freq(raw_line)
            if word is not None:
                append_line(output_file, '%s\t%d' % (word, freq))

    complete_time = datetime.datetime.now()
    print('extracting completed...')
    print('time elapsed: {0}'.format(complete_time - start_time))


def extract_unigrams(data_dir):

    cwd = os.getcwdu()
    print('cwd: {0}'.format(cwd))
    print('change wd to: {0}'.format(data_dir))
    os.chdir(data_dir)

    output_dir = './1gram/'
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    for f in glob.glob('*1gram*.txt'):
        # print(f)
        # print(os.path.getsize(f))
        name, ext = os.path.splitext(f)
        output_file = output_dir + name + '-unigram.txt'
        print('generatint to ' + output_file)

        if not os.path.exists(output_file):
            build_unigram(f, output_file)
        else:
            print(output_file + ' already exits...')

    print('change wd back to: {0}'.format(cwd))
    os.chdir(cwd)


if __name__ == '__main__':
    extract_unigrams(r'D:\andersc\downloads\googlebooks-eng-1M-ngrams\ngrams\token-freq')
