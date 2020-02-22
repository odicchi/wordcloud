from janome.tokenizer import Tokenizer
from collections import defaultdict

def counter(texts):
    t = Tokenizer()
    words_count = defaultdict(int)
    words = []
    for text in texts:
        tokens = t.tokenize(text)
        for token in tokens:
            # 品詞から形容詞と名詞だけ抽出
            pos = token.part_of_speech.split(',')[0]
            if pos in ['形容詞','動詞']:
                # 必要ない単語を省く(実際の結果を見てから不必要そうな単語を記載しました)
                if token.base_form not in ["こと", "よう", "そう", "これ", "それ"]:
                    words_count[token.base_form] += 1
                    words.append(token.base_form)
    return words_count, words

def parseWordCloudText(textList):
    return " ".join(textList) if type(textList) is list else ""