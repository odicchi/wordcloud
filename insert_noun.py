from mongo_dao import MongoDAO
import codecs

mongo = MongoDAO("db","noun")

dict_path = './dict/noun_dict.trim'

with codecs.open(dict_path, "r", "utf-8") as f:
    for line in f:
        d = line[:-1].split('\t')
        print(d)
        if d[1] == 'n':
            d.append(-1)
        elif d[1] == 'p':
            d.append(1)
        else:
            d.append(0)

        mongo.insert_one({"word": d[0], "np": d[1], "evaluation": d[2], "score": d[3]})