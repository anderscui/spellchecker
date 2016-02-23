import time
import datetime

from common import io


def read_line(line, n=1, version='20090715'):
    parts = line.strip().split('\t')
    return parts[0], int(parts[2])


def merge_lines(lines):
    tokens = []
    cur_token = None
    cur_token_count = 0
    for line in lines:
        if cur_token == None:
            cur_token = line[0]
            cur_token_count = line[1]
        else:
            if cur_token == line[0]:
                cur_token_count += line[1]
            else:
                tokens.append((cur_token, cur_token_count))

                cur_token = line[0]
                cur_token_count = line[1]

    tokens.append((cur_token, cur_token_count))
    return tokens


#file_path = '../data/ngrams/googlebooks-eng-1M-1gram-20090715-0.csv'
# i = 0
# lines = []
# with open(file_path) as f:
#     for line in f:
#         # time.sleep(1)
#         # print(line.strip())
#         lines.append(line.strip())
#
#         i += 1
#         if i >= 100000:
#             break
#
# io.write_str('../data/ngrams/1gram_data_less.csv', '\n'.join(lines))

def append_line(file_path, line):
    with open(file_path, "a") as f:
        f.write(line)

print(datetime.datetime.now())

# file_path = './1gram_data_less.csv'
# out_file = './1gram_token_less.txt'

# file_path = '../data/ngrams/googlebooks-eng-1M-1gram-20090715-0.csv'
# out_file = './googlebooks-eng-1M-1gram-20090715-0-out.txt'

file_path = '../data/ngrams/googlebooks-eng-1M-1gram-20090715-1.csv'
out_file = './googlebooks-eng-1M-1gram-20090715-1-out.txt'
with open(file_path) as f:

    cur_token = None
    cur_token_count = 0

    for raw_line in f:

        line = read_line(raw_line)
        if cur_token == None:
            cur_token = line[0]
            cur_token_count = line[1]
        else:
            if cur_token == line[0]:
                cur_token_count += line[1]
            else:
                # unigrams.append((cur_token, cur_token_count))
                append_line(out_file, '%s %d\n' % (cur_token, cur_token_count))

                cur_token = line[0]
                cur_token_count = line[1]

    append_line(out_file, '%s %d\n' % (cur_token, cur_token_count))

print(datetime.datetime.now())
