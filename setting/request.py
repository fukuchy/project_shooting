import requests
from . import paramater as para
from . import player as p
POST_URL = "http://127.0.0.1:8888"

def request():

    name = p.player.name
    score = para.point
    request_body = {"name":name,"score":score}

    res = requests.post(POST_URL,json=request_body)
    print(res.text)

#TODO:inputを使ってcsvに書き込む