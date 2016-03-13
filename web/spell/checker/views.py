# coding=utf-8
import os
import time

import operator
from caching.base import cached
from django.shortcuts import render

from django.conf import settings

is_cached = False


def get_obj():
    time.sleep(2)
    return 'hello'


def data_dir():
    # return os.path.join(settings.BASE_DIR, '../data/')
    return r'D:\andersc\github\spellchecker\data'


print(data_dir())
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


def datafile(name, sep='\t'):
    """Read key, vlaue pairs from file."""
    for line in file(os.path.join(data_dir(), name)):
        yield line.split(sep)


def avoid_long_words(key, N):
    """Estimate the probability of an unknown word."""
    return 10. / (N * 10 ** len(key))


def get_primary_dict():
    return Pdist(datafile('ngrams/primary_dict.txt'), None, avoid_long_words)


def get_valid_prefixes():
    return set(w[:i] for w in Pw for i in xrange(len(w)+1))


def get_p1edit():
    """the prob of single edits"""
    return Pdist(datafile('norvig/count_1edit.txt'))


Pw = cached(get_primary_dict, 'primary_dict', 600)
PREFIXES = cached(get_valid_prefixes, 'prefixes', 600)
# P1edit = cached(get_p1edit, 'p1edit', 600)
P1edit = get_p1edit()

# def cPw(word, prev):
#     """
#     The conditional probability P(word | previous word)
#     """
#     try:
#         return P2w[prev + ' ' + word] / float(Pw[prev])
#     except KeyError:
#         return Pw(word)
#
# # TODO: cachable
# # P2w = Pdist(datafile('../data/norvig/count_2w.txt'), N)
# P2w = Pdist(datafile('../data/ngrams/bigram_dict_less.txt'), None)


# common error rate
p_spell_error = 1./20

def Pedit(edit):
    # prob of 'right is right'
    if edit == '':
        return 1. - p_spell_error

    return p_spell_error * product(P1edit(e) for e in edit.split('+'))


alphabet = 'abcdefghijklmnopqrstuvwxyz'


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


def correct(w):

    candicates = edits(w).items()
    c, edit = max(candicates, key=lambda (c, e): Pedit(e) * Pw(c))
    return [c]


def index(request):

    word = request.GET.get('word', '')
    if not word:
        return render(request, 'checker/index.html', {'page_name': 'checker.index'})

    c = correct(word)
    return render(request, 'checker/index.html', {'page_name': 'checker.index',
                                                  'word': word,
                                                  'corrections': c})


def stats(request):
    return render(request, 'checker/stats.html', {'page_name': 'checker.stats'})
