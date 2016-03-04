import datetime
import glob
import os
import time

from common.io import append_line, read_lines, write_str
from ngrams import read_word_freq

start_year = 1900


def extract_tokens(data_file, output_file):
    """
    extract token stats in the data_file, save it in output_file.
    :param data_file:
    :param output_file:
    """
    start_time = datetime.datetime.now()
    print(start_time)
    print('extracting started...')

    with open(data_file) as f:

        cur_token = None
        cur_token_count = 0

        buf = []

        for raw_line in f:

            token, freq = read_word_freq(raw_line, start_year)
            if token is None:
                continue

            if cur_token is None:
                cur_token = token
                cur_token_count = freq
            else:
                if cur_token == token:
                    cur_token_count += freq
                else:
                    append_line(output_file, '%s\t%d' % (cur_token, cur_token_count))

                    cur_token = token
                    cur_token_count = freq

        if cur_token:
            append_line(output_file, '%s\t%d' % (cur_token, cur_token_count))

    complete_time = datetime.datetime.now()
    print('extracting completed...')
    print('time elapsed: {0}'.format(complete_time - start_time))


def extract_dir_tokens(data_dir, output_dir):

    cwd = os.getcwdu()
    print('cwd: {0}'.format(cwd))
    print('change wd to: {0}'.format(data_dir))
    os.chdir(data_dir)

    output_dir = './output/'
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    for f in glob.glob('*.csv'):
        # print(f)
        # print(os.path.getsize(f))
        name, ext = os.path.splitext(f)
        output_file = output_dir + name + '-out.txt'
        print('generatint to ' + output_file)

        if not os.path.exists(output_file):
            extract_tokens(f, output_file)
        else:
            print(output_file + ' already exits...')

    print('change wd back to: {0}'.format(cwd))
    os.chdir(cwd)

# file_path = '../data/ngrams/googlebooks-eng-1M-4gram-20090715-0.csv'
# lines = list(read_lines(file_path, 100000))
# write_str('./4gram_data_less.csv', ''.join(lines))

# file_path = './1gram_data_less.csv'
# out_file = './1gram_token_less.txt'
# file_path = '../data/ngrams/googlebooks-eng-1M-1gram-20090715-0.csv'
# out_file = './googlebooks-eng-1M-1gram-20090715-0-out.txt'
# file_path = '../data/ngrams/googlebooks-eng-1M-1gram-20090715-2.csv'
# out_file = './googlebooks-eng-1M-1gram-20090715-2-out.txt'

# extract_tokens(file_path, out_file)

extract_dir_tokens(r'D:\andersc\downloads\googlebooks-eng-1M-ngrams\1gram', '.')
