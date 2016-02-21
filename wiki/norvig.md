
# How to Write a Spelling Corrector

## Overview

See [original post](http://norvig.com/spell-correct.html)

Norvig wanted to develop a **toy spelling corrector** that achieves 80% or 90% accuracy at a processing speed of at least 10 words per second, in less than a page of code.

The Python version is in 21 lines.

```python
import re, collections

def words(text): return re.findall('[a-z]+', text.lower()) 

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

NWORDS = train(words(file('big.txt').read()))

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)
```

Examples:

```
correct('speling') -> spelling
correct('korrecter') -> corrected
```

## How it Works

Given a word, we are trying to choose the most likely spelling correction, there is **no way to know for sure**, which suggests we **use probabilities**.

We will say that we are trying to find the correction *c*, out of all possible corrections, that maximizes the probability of *c* given the original word *w*.

argmax_c P(c|w)

This is really the general idea. By [Bayes' Therem](http://en.wikipedia.org/wiki/Bayes'_theorem) this is equivalent to:

argmax_c P(w|c) P(c) / P(w)

Since P(w) is the same for every possible *c*, we can just ignore it, giving:

argmax_c P(w|c) P(c)

The expression consists of three parts:

1. P(c), called **language model**, think of "how likely is *c* to appear in an English text?", so P('the') is relatively high, while P('abcde') would be near zero.
2. P(w|c), called **error model**, recall that *c* is a possible correction, so think of "how likely is it that the author would type *w* by mistake when *c* was intended?"
3. argmax_c, the control mechanism, enumerate all **feasible values** of *c*, and then choose the one that gives the best combined probability score.

This expression is the starting point. We can try to improve the models of 3 parts.

## Implementation

