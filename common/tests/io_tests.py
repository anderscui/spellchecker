from common.io import zip_extract_all


def test_zip_extract_all():
    f = '1M-total.zip'
    target = '.'
    zip_extract_all(f, target)


def test_zip_extract_large_all():
    f = 'D:/andersc/downloads/googlebooks-eng-1M-ngrams/googlebooks-eng-1M-1gram-20090715-9.csv.zip'
    target = '.'
    zip_extract_all(f, target)


if __name__ == '__main__':
    # test_zip_extract_all()
    import datetime

    print(datetime.datetime.now())
    test_zip_extract_large_all()
    print(datetime.datetime.now())
