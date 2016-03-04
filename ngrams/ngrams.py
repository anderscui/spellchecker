import re

re_en_word = re.compile(r"^[a-zA-Z-'.]+$")


def is_english_word(w):
    return re_en_word.match(w) is not None


# ngram TAB year TAB match_count
def read_word_freq(line, start_year=None, to_lower=True):
    parts = line.split('\t')

    if start_year and int(parts[1]) < start_year:
        return None, None

    if is_english_word(parts[0]):
        if to_lower:
            return parts[0].lower(), int(parts[2])
        else:
            return parts[0], int(parts[2])
    else:
        return None, None
