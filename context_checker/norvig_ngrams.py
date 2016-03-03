# coding=utf-8
"""Ngram Samples by Peter Norgiv.
Beautiful Data
Copyright ©2009 O'Reilly Media, Inc.
"""
import operator
import re
from math import log10


def memo(f):
    """
    Memoize function f.
    """
    table = {}

    def fmemo(*args):
        if args not in table:
            table[args] = f(*args)
        return table[args]

    fmemo.memo = table
    return fmemo


## Word Segmentation
@memo
def segment(text):
    """
    Return a list of words that is the best segmentation of text.
    """
    if not text:
        return []

    candidates = ([first] + segment(remaining) for first, remaining in splits(text))
    return max(candidates, key=Pwords)


def Pwords(words):
    """
    The Naive Bayes probability of a sequence of words.
    :param words: a list of words
    """
    return product(Pw(w) for w in words)


## Helpers
def product(nums):
    return reduce(operator.mul, nums, 1)


class Pdist(dict):
    """A probability distribution estimated from counts in datafile."""
    def __init__(self, data=[], N=None, missingfn=None):
        for key, count in data:
            self[key] = self.get(key, 0) + int(count)
        self.N = float(N or sum(self.itervalues()))
        self.missingfn = missingfn or (lambda k, N: 1. / N)

    def __call__(self, key):
        if key in self:
            return self[key] / self.N
        else:
            return self.missingfn(key, self.N)


def splits(text, L=20):
    return [(text[:i + 1], text[i + 1:]) for i in xrange(min(len(text), L))]


def datafile(name, sep='\t'):
    """Read key, vlaue pairs from file."""
    for line in file(name):
        yield line.split(sep)


def avoid_long_words(key, N):
    """Estimate the probability of an unknown word."""
    return 10. / (N * 10 ** len(key))


N = 1024908267229  ## Number of tokens

# TODO: cachable
Pw = Pdist(datafile('../data/norvig/count_1w.txt'), N, avoid_long_words)


# Pw['unregarded'] = 7557
# N += Pw['unregarded']

def cPw(word, prev):
    """
    The conditional probability P(word | previous word)
    """
    try:
        return P2w[prev + ' ' + word] / float(Pw[prev])
    except KeyError:
        return Pw(word)

# TODO: cachable
P2w = Pdist(datafile('../data/norvig/count_2w.txt'), N)


# print(cPw('sit', 'to') * cPw('down', 'sit') / cPw('sitdown', 'to'))

def sPw(s, n=2):
    if not s:
        return None

    words = ['<S>'] + s.lower().split(' ')
    print(words)
    return sum([log10(cPw(words[i], words[i - 1])) for i in xrange(1, len(words))])


@memo
def segment2(text, prev='<S>'):
    """Return (log P(words), words), where words is the best segmentation."""
    if not text:
        return 0.0, []
    candidates = [combine(log10(cPw(first, prev)), first, segment2(rem, first))
                  for first, rem in splits(text)]

    return max(candidates)


def combine(Pfirst, first, (Prem, rem)):
    return Pfirst + Prem, [first] + rem


def corrections(text):
    """
    spell correct all words in text.
    :param text: the input text
    :return: the corrected text
    """
    return re.sub('[a-zA-Z]+', lambda m: correct(m.group(0)), text)


def correct(w):

    candicates = edits(w).items()
    c, edit = max(candicates, key=lambda (c, e): Pedit(e) * Pw(c))
    return c

# common error rate
p_spell_error = 1./20


def Pedit(edit):
    # prob of 'right is right'
    if edit == '':
        return (1. - p_spell_error)

    return p_spell_error * product(P1edit(e) for e in edit.split('+'))


# the prob of single edits
P1edit = Pdist(datafile('../data/norvig/count_1edit.txt'))

alphabet = 'abcdefghijklmnopqrstuvwxyz'
alphabet = 'ab'
# TODO: cachable
PREFIXES = set(w[:i] for w in Pw for i in xrange(len(w)+1))


def edits(word, d=2):
    results = {}

    def editsR(hd, tl, d, edits):
        def ed(L, R):
            return edits + [R + '|' + L]
        C = hd+tl
        # if C is in the dict
        if C in Pw:
            e = '+'.join(edits)
            if C not in results:
                results[C] = e
            else:
                results[C] = max(results[C], e, key=Pedit)

        if d <= 0:
            return

        extensions = [hd+c for c in alphabet if hd+c in PREFIXES]
        # previous char
        p = (hd[-1] if hd else '<')

        # insertion
        for h in extensions:
            editsR(h, tl, d-1, ed(p+h[-1], p))
        if not tl:
            return

        # deletion
        editsR(hd, tl[1:], d-1, ed(p, p+tl[0]))

        # replacement
        for h in extensions:
            # match
            if h[-1] == tl[0]:
                editsR(h, tl[1:], d, edits)
            else:
                editsR(h, tl[1:], d-1, ed(h[-1], tl[0]))

        # transpose
        if len(tl) >= 2 and tl[0] != tl[1] and hd+tl[1] in PREFIXES:
            editsR(hd+tl[1], tl[0]+tl[2:], d-1, ed(tl[1]+tl[0], tl[0:2]))

    # body of edits
    editsR('', word, d, [])
    return results


## test cases
def test_sentence_pw():
    # the house is small vs. small the is house
    print(sPw('the house is small'))
    print(sPw('small the is house'))

    print(sPw('I am going home'))
    print(sPw('I am going house'))


def test_segment():
    print(segment(
            'faroutintheunchartedbackwatersoftheunfashionableendofthewesternspiralarmofthegalaxyliesasmallunregardedyellowsun'))
    print(segment('tellusyourideas'))
    print(segment('itisatruthuniversallyacknowledged'))
    print(segment('iaskyoutositdown'))

    print(segment2(
        'faroutintheunchartedbackwatersoftheunfashionableendofthewesternspiralarmofthegalaxyliesasmallunregardedyellowsun'))
    print(segment2('tellusyourideas'))
    print(segment2('itisatruthuniversallyacknowledged'))
    print(segment2('iaskyoutositdown'))


def test_edits():
    print(edits('adiabatic'))
    print(edits('acommodations'))


def test_corrections():
    # print(Pw('good'))
    # print(Pw('goood'))
    # print(Pw('spelling'))
    # print(Pw('speling'))
    #
    # print(correct('vokabulary'))
    # print(correct('goood'))
    # print(correct('speling'))

    # ref: http://textblob.readthedocs.org/en/dev/quickstart.html#spelling-correction
    # TODO: too poor
    print(corrections('I havv goood speling!'))

    # Norvig's sample
    # 13 of 15 are OK, but acommodations and mispellings are left there.
    print(corrections('Thiss is a teyst of acommodations for korrections of mispellings of particuler wurds.'))


if __name__ == '__main__':
    # test_sentence_pw()
    # test_segment()
    # test_edits()

    test_corrections()
    # for k, v in edits('as').items():
    #     print(k, v)
