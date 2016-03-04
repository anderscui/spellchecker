from common.persistence import from_pickle


def check_dic_freq():
    en_dict = from_pickle('../data/ngrams/en_dict.pkl')
    print(en_dict['the'])
    print(en_dict['of'])
    print(en_dict['and'])
    print(en_dict['to'])
    print(en_dict['a'])
    print(en_dict['in'])
    print(en_dict['for'])
    print(en_dict['click'])

    print(en_dict["doesn't"])
    print(en_dict["can't"])
    print(en_dict["cannot"])

    print(en_dict["first-class"])

    # non-real words
    print(en_dict['good'])
    print(en_dict['goood'])
    print(en_dict['spelling'])
    print(en_dict['speling'])


if __name__ == '__main__':
    check_dic_freq()
