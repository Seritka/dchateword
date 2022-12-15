from transformers import TextClassificationPipeline, BertForSequenceClassification, AutoTokenizer
import json

model_name = 'sgunderscore/hatescore-korean-hate-speech'
model = BertForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
pipe = TextClassificationPipeline(
        model = model,
        tokenizer = tokenizer,
        device = -1, # gpu: 0
        return_all_scores = True,
        function_to_apply = 'sigmoid',
        top_k=1)

comments = []

with open('./dc.json', 'r', encoding='utf8') as file:
    data = json.load(file)
    for i in data:
        for j in i["comments"]:
            comments.append(str(j["contents"]).replace("\n", " "))

hatespeechs = []

for i in comments:
    try:
        for result in pipe(i)[0]:  # type: ignore
            hatespeechs.append({ 'comment': i, 'hatescores': result })
            with open('./hatespeech.json', 'w', encoding='utf8') as outfile:
                json.dump(hatespeechs, outfile, indent=4, ensure_ascii=False)
    except RuntimeError:
        continue

