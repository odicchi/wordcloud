import json
import config
from requests_oauthlib import OAuth1Session
from time import sleep
import emoji
from mongo_dao import MongoDAO

# 絵文字を除去する
def remove_emoji(src_str):
    return ''.join(c for c in src_str if c not in emoji.UNICODE_EMOJI)

# APIキー設定(別ファイルのconfig.pyで定義しています)
CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET

# 認証処理
twitter = OAuth1Session(CK, CS, AT, ATS)  

# タイムライン取得エンドポイント
url = "https://api.twitter.com/1.1/search/tweets.json"  

# 取得するキーワード
keyword = '転校少女'

# パラメータの定義
params = {'q': keyword,
          'count': 200}

# arg1:DB Name
# arg2:Collection Name
mongo = MongoDAO("db", "tenkou")
mongo.delete_many({})

# 最新の200件を取得／2回目以降はparams['max_id']に設定したIDより古いツイートを取得
for j in range(100):
    res = twitter.get(url, params=params)
    if res.status_code == 200:
        # API残り回数
        limit = res.headers['x-rate-limit-remaining']
        print("API remain: " + limit)
        if limit == 1:
            sleep(60*15)

        n = 0
        result = json.loads(res.text)
        # ツイート単位で処理する
        tweets = result['statuses']
        for tweet in tweets:
            # 絵文字があると、wordcloudが使用できないため、削除する
            tweet['text'] = remove_emoji(tweet['text'])
            # ツイートデータを丸ごと登録
            mongo.insert_one(tweet)
        
            if len(tweets) >= 1:
                params['max_id'] = tweets[-1]['id']-1
