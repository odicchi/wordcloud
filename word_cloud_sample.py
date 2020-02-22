# coding:utf-8
import csv
from janome.tokenizer import Tokenizer
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from bs4 import BeautifulSoup
from collections import Counter, defaultdict
import codecs
from mongo_dao import MongoDAO
import numpy as np
from PIL import Image

def counter(texts):
    t = Tokenizer()
    words_count = defaultdict(int)
    words = []
    for text in texts:
        tokens = t.tokenize(text)
        for token in tokens:
            # 品詞から名詞だけ抽出
            pos = token.part_of_speech.split(',')[0]
            if pos in ['形容詞','動詞']:
                # 必要ない単語を省く(実際の結果を見てから不必要そうな単語を記載しました)
                if token.base_form not in ["こと", "よう", "そう", "これ", "それ"]:
                    words_count[token.base_form] += 1
                    words.append(token.base_form)
    return words_count, words

target = 'tenkou'
mongo = MongoDAO("db", target)
results= mongo.find(projection={"text":1})

texts = []
for result in results:
    s = result['text'].replace('\n','')
    text = s.split('http')
    texts.append(text[0])
    
# with codecs.open('./output/tweet_data', 'r', 'utf-8') as f:
#     reader = csv.reader(f, delimiter='\t')
#     texts = []
#     for row in reader:
#         if(len(row) > 0):
#             text = row[0].split('http')
#             texts.append(text[0])

words_count, words = counter(texts)
text = ' '.join(words)
print(text)
# StopWords
stop_words = ['RT','@', '//','NECOPLASTIC', 'ネコプラ', 'ネコ','chuLa', 'FESTIVE','FES', 'TIVE',
            'ナナランド','JYAPON','ナナ','ランド','JAPONISM','JYA','NEO','PON','なんキニ','なん',
            'キニ','する','とる','てる','くる','なる','いる','れる','せる','おる','どる','ぶる']
# fontは自分の端末にあるものを使用する
font_path = 'C:\\WINDOWS\\Fonts\\meiryo.ttc'
# mask画像のパス
# mask_path = './mask/' + target + '3.jpg'
mask_path = './mask/wordcloud_07.png'
mask_image = np.array(Image.open( mask_path ))

wordcloud = WordCloud(background_color="white",font_path=font_path,mask=mask_image,contour_color='steelblue',
                    contour_width=3,width=900, height=500,stopwords=set(stop_words)).generate(text)

wordcloud.to_file("./output_wordcloud/wordcloud_" + target + "3.png")