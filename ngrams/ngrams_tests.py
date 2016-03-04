from ngrams import is_english_word, read_word_freq


def test_is_english_word():
    assert is_english_word('a')
    assert is_english_word('word')
    assert is_english_word('first-class')
    assert is_english_word("don't")
    assert is_english_word('u.s.a.')

    assert is_english_word('B')
    assert is_english_word('Good')


def test_read_word_freq_lower():
    line = 'test\t1999\t10\t6'
    wf = read_word_freq(line)
    assert wf == ('test', 10)

    line = 'test\t1999\t10\t6'
    wf = read_word_freq(line, 1999)
    assert wf == ('test', 10)

    line = 'test\t1999\t10\t6'
    wf = read_word_freq(line, 2000)
    assert wf == (None, None)


def test_read_word_freq_upper():
    line = 'Test\t1999\t10\t6'
    wf = read_word_freq(line)
    assert wf == ('Test', 10)

    line = 'Test\t1999\t10\t6'
    wf = read_word_freq(line, to_lower=True)
    assert wf == ('test', 10)

    line = 'test\t1999\t10\t6'
    wf = read_word_freq(line, 1999)
    assert wf == ('test', 10)

    line = 'test\t1999\t10\t6'
    wf = read_word_freq(line, 2000)
    assert wf == (None, None)


def test_read_word_freq_en_word():
    line = 'test\t1999\t10\t6'
    wf = read_word_freq(line)
    assert wf == ('test', 10)

    line = 't@est\t1999\t10\t6'
    wf = read_word_freq(line)
    assert wf == ('t@est', 10)

    line = 't@est\t1999\t10\t6'
    wf = read_word_freq(line, en_word_only=True)
    assert wf == (None, None)
