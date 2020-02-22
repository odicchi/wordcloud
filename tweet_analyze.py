import MeCab
from mongo_dao import MongoDAO
import word_cloud
from wordcloud import WordCloud

target = "tenkou"
#MeCab準備
tagger = MeCab.Tagger("-Ochasen")

# mongoDBからデータを取得する
mongo = MongoDAO("db", target)

target_results = mongo.find()

# 解析結果の格納用
positive_words = []
negative_words = []
neutral_words = []
tweet_score = 0

# DBの接続先を辞書データに変更
mongo = MongoDAO("db", "noun")

for target_result in target_results:
    text = target_result['text']

    mecab_results = tagger.parse(text)

    for result in mecab_results.split('\n'):

        word = result.split('\t')[0]
        
        mongo_result = mongo.find_one(filter={"word":word})

        if type(mongo_result) is dict:
            tweet_score += mongo_result['score']
            if mongo_result['np'] == 'n':
                negative_words.append(word)
            elif mongo_result['np'] == 'p':
                positive_words.append(word)
            elif mongo_result['np'] == 'e':
                neutral_words.append(word)
        else:
            neutral_words.append(word)

stop_words = ['RT','@', '//','NECOPLASTIC', 'ネコプラ', 'ネコ','chuLa', 'FESTIVE','FES', 'TIVE',
            'ナナランド','JYAPON','ナナ','ランド','JAPONISM','JYA','NEO','PON','なんキニ','なん',
            'キニ','する','とる','てる','くる','なる','いる','れる','せる','おる','どる','ぶる']
# fontは自分の端末にあるものを使用する
font_path = 'C:\\WINDOWS\\Fonts\\meiryo.ttc'

# ポジティブワードでワードクラウドを作成
wordcloud = WordCloud(background_color="white",font_path=font_path,contour_color='steelblue', collocations = False,
                    contour_width=3,width=900, height=500,stopwords=set(stop_words)).generate(word_cloud.parseWordCloudText(positive_words))
wordcloud.to_file("./output_wordcloud/wordcloud_" + target + "_positive.png")

# ネガティブワードでワードクラウドを作成
wordcloud = WordCloud(background_color="white",font_path=font_path,contour_color='steelblue', collocations = False,
                    contour_width=3,width=900, height=500,stopwords=set(stop_words)).generate(word_cloud.parseWordCloudText(negative_words))
wordcloud.to_file("./output_wordcloud/wordcloud_" + target + "_negative.png")
