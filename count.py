import json

count = 0

with open('./dc.json', 'r', encoding='utf8') as file:
    data = json.load(file)
    for i in data:
        count += i["comment_count"]
    print("total comment count: ", count)