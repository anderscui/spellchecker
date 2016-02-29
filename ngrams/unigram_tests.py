from common.persistence import from_pickle

en_dict = from_pickle('../data/en_dict.pkl')
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
