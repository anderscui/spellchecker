import re

re_en_word = re.compile(r"^[a-zA-Z-'.]+$")
re_en_ngram = re.compile(r"^[a-zA-Z-'. ]+$")


def is_english_word(w):
    return re_en_word.match(w) is not None


def is_english_ngram(w):
    return re_en_ngram.match(w) is not None

# ngram TAB year TAB match_count
def read_word_freq(line, start_year=None, en_word_only=False, to_lower=False):
    parts = line.split('\t')

    if start_year and int(parts[1]) < start_year:
        return None, None

    if en_word_only and (not is_english_word(parts[0])):
        return None, None

    if to_lower:
        return parts[0].lower(), int(parts[2])
    else:
        return parts[0], int(parts[2])
