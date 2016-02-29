import checker


def test_words():
    text = 'I figured they and many others could benefit from an explanation.'
    words = checker.words(text)
    assert len(words) == 11


def test_train():
    text = 'A friend in need is a friend indeed'
    features = checker.words(text)
    print features
    model = checker.train(features)
    print model
    assert 'friend' in model
    assert 'friends' not in model

    print model['friend']

    assert model['friend'] == 2
    assert model['a'] == 2
    assert model['need'] == 1
    assert model['friends'] == 0


def test_correct():
    print checker.correct('speling')
    print checker.correct('korrecter')
    print checker.correct('lates')
    print checker.correct('testt')
    print checker.correct('embaras')
    print checker.correct('colate')
    print checker.correct('generataed')
    print checker.correct('thay')


if __name__ == '__main__':
    # test_train()
    test_correct()
