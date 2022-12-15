import json
from wordcloud import WordCloud
from konlpy.tag import Okt
from collections import Counter

comments = []

with open('./dc.json', 'r', encoding='utf8') as file:
    data = json.load(file)
    for i in data:
        for j in i["comments"]:
            comments.append(str(j["contents"]).replace("\n", " "))

okt = Okt()

# twitter함수를 통해 읽어들인 내용의 형태소를 분석한다.
sentences_tag = []
sentences_tag = okt.pos('\n'.join(comments))

noun_adj_list = []


# tag가 명사이거나 형용사인 단어들만 noun_adj_list에 넣어준다.
for word, tag in sentences_tag:
    if tag in ['Noun', 'Adjective']:
        noun_adj_list.append(word)

counts = Counter(noun_adj_list)
tags = counts.most_common(1000)

wc = WordCloud(font_path="./NEXONLv1GothicRegular.ttf", background_color="white", max_font_size=60)
cloud = wc.generate_from_frequencies(dict(tags))
cloud.to_file('test.jpg')
