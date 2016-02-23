# 1gram, line
# '#	1574	1	1	1'

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


if __name__ == '__main__':
    l1 = '#	1574	1	1	1'
    lr = read_line(l1)

    assert len(lr) == 2
    assert lr[0] == '#'
    assert lr[1] == 1

    # multilines
    lines = [('#', 5), ('#', 9), ('#', 10), ('$1380', 3), ('$2195', 10), ('$2195', 20)]
    line_tokens = merge_lines(lines)

    assert len(line_tokens) == 3

    assert line_tokens[0][0] == '#'
    assert line_tokens[0][1] == 24

    assert line_tokens[1][0] == '$1380'
    assert line_tokens[1][1] == 3

    assert line_tokens[2][0] == '$2195'
    assert line_tokens[2][1] == 30
