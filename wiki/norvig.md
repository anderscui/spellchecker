
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

### dictionary

First we need to calulate P(c), we need a kind of big dictionary(via corpus), here Norvig merges some text resources, such as public domain books from [Project Gutenberg](http://www.gutenberg.org/wiki/Main_Page), list of most frequent words from [Wiktionary](http://en.wiktionary.org/wiki/Wiktionary:Frequency_lists), and the [British Natinoal Corpus](http://www.kilgarriff.co.uk/bnc-readme.html).

```python
def words(text): return re.findall('[a-z]+', text.lower()) 

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

NWORDS = train(words(file('big.txt').read()))
```

Now, `NWORDS[w]` holds a count of how many times the word `w` has been seen. There is one complication: novel words which are not seen in training corpus.

What happens with a perfectly good word of English that wasn't seen in our training data? Since the training data is always limited, this case always happens. **It would be bad form to just say the probability of a word is zero because we haven't seen it yet.**

We need to do something called **smoothing**, the easist approach is adding one to all the words, this is implemented by defaultdict.

### possible corrections

Now we need to enumerate the possible corrections `c` of a given word `w`. It is common to talk of the **[edit distance](https://en.wikipedia.org/wiki/Edit_distance)** between two words: the number of edits it would take to turn one into the other. An edit could be a deletion, transposition, alteration or an insertion:

```python
def edits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)
```

For a word of length `n`, we could have 54`n`+25 corrections at most, for 'something' we get 494, it is certainly feasible. And further, based on edits1, we can also get the two edits words:

```python
def edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1))
```

Now we'are starting to get into some serious computation: `len(edits2('something')) = 114324`. But we do get good coverage: of the 270 test cases, only 3 have an edit distance greater than 2, i.e. edits2 will cover 98.9% of the cases, that's good enough for our aim. Since we aren't going beyond edit distance 2, we can do a small optimization: only keep the candidates that are actually **know words**.

```python
def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)
```

Using this function, known_edits2('something') is a set of just 4 words: {'smoothing', 'seething', 'something', 'soothing'}, rather than the set of 114,324 words.

### error model

Now the only part left is the error model, P(w|c). This is the tricky part - we have no training data to build a model of spelling errors.

We may have some intuitions: mistaking one vowel for another is more probable than mistaking two consonants; making an error on the first letter of a word is less probable; due to finger slipping, P(best|nest) > P(west|nest), etc. But we had no numbers to back that up.

So we can(have to) take a shortcut:

```python
def known(words): return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)
``` 

## Evaluation

training & eval dataset.

