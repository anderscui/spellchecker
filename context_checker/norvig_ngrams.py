# coding=utf-8
"""Ngram Samples by Peter Norgiv.
Beautiful Data
Copyright ©2009 O'Reilly Media, Inc.
"""
import operator
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


P2w = Pdist(datafile('../data/norvig/count_2w.txt'), N)


# print(cPw('sit', 'to') * cPw('down', 'sit') / cPw('sitdown', 'to'))

def sPw(s, n=2):
    if not s:
        return None

    words = ['<S>'] + s.lower().split(' ')
    print(words)
    return sum([log10(cPw(words[i], words[i-1])) for i in xrange(1, len(words))])

# print(cPw('sit', 'to') * cPw('down', 'sit') / cPw('sitdown', 'to'))

# the house is small vs. small the is house
print(sPw('the house is small'))
print(sPw('small the is house'))

print(sPw('I am going home'))
print(sPw('I am going house'))


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

#
if __name__ == '__main__':
    # print(segment('whereareyoufrom'))
    print(segment(
            'faroutintheunchartedbackwatersoftheunfashionableendofthewesternspiralarmofthegalaxyliesasmallunregardedyellowsun'))
    print(segment('tellusyourideas'))
    print(segment('itisatruthuniversallyacknowledged'))
    print(segment('iaskyoutositdown'))

    print(segment2('faroutintheunchartedbackwatersoftheunfashionableendofthewesternspiralarmofthegalaxyliesasmallunregardedyellowsun'))
    print(segment2('tellusyourideas'))
    print(segment2('itisatruthuniversallyacknowledged'))
    print(segment2('iaskyoutositdown'))
