import matplotlib.pylab as plt
import matplotlib.font_manager as fm
import numpy as np
import json

# → 여성, 성소수자, 지역, 인종/국적, 종교, 연령, 남성의 7가지 이며 기타 혐오발언, 단순 악플, 일반 댓글(clean)의 3가지 유형이 추가로 제공됩니다.

total = { '여성/가족': 0, '성소수자': 0, '지역': 0, '인종/국적': 0, '종교': 0, '연령': 0, '기타 혐오발언': 0, '단순 악플': 0, 'None': 0  }

with open('./hatespeech.json', 'r', encoding='utf8') as file:
    data = json.load(file)
    for i in data:
        label = i["hatescores"]["label"]
        if label in total:
            total[label] += 1

total = sorted(total.items(), key = lambda item: item[1], reverse = True)
for i in total:
    print("유형: "+ i[0].replace("None", "혐오발언 없음")+",", str(i[1])+"개")

font_name = fm.FontProperties(fname='./NEXONLv1GothicRegular.ttf') # type: ignore

x = np.arange(9)
keys = [i[0].replace("None", "혐오발언 없음") for i in total]
values = [i[1] for i in total]

plt.bar(x, values)
plt.xticks(x, keys, fontproperties=font_name)
plt.title("혐오발언 유형", fontproperties=font_name)
plt.show()