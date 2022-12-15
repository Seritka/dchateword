import asyncio
import requests
import json
from lxml import html
import dc_api

def req(board_id, document_id):
    _headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    }
    _url = "https://m.dcinside.com/board/{}/{}".format(board_id, document_id)
    req = requests.get(url=_url,headers=_headers)  # type: ignore
    tree = html.fromstring(req.content)
    return { 'subject': tree.xpath("//span[starts-with(@class, 'title_subject')]")[0].text, 'source': tree.xpath("/html/body/div[2]/div[3]/main/section/article[2]/div[1]/div/div[1]/div[1]/div/div/b")[0].text }

list = []
board_id="dcbest"
file = './dc_total.json'

async def run():
  async with dc_api.API() as api:
    async for index in api.board(board_id=board_id, num=1000):
      comments = []
      async for com in index.comments():
        if com.contents != "":
          dict = {
            'author': com.author,
            'contents': str(com.contents).replace("- dc App", "").rstrip()
          }
          comments.append(dict)
      index.subject = req(board_id, index.id)['subject']
      source = str(req(board_id, index.id)['source']).replace("출처:", "").strip()
      list.append({ 'id': int(index.id), 'subject': index.subject, 'source': source, 'time': index.time.timestamp(), 'comments': comments, 'comment_count': int(index.comment_count) })
      print({ 'id': index.id, 'subject': index.subject, 'source': source, 'time': index.time.timestamp() })
      with open(file, 'w', encoding='utf8') as outfile:
        json.dump(list, outfile, indent=4, ensure_ascii=False)
    print("Finish!!!")

asyncio.run(run())