import requests
import json
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import requests

from elasticsearch import Elasticsearch, helpers
# defualt mappings in elasticsearch
# you can change to fit your database

delta = timedelta(days=1)
yesterday = datetime.now() - delta + timedelta(hours=9)
yesterday = yesterday.strftime("%Y%m%d")
INDEX = f'news_{yesterday}'

es = Elasticsearch('http://elasticsearch:9200')

mappings = {
    "settings": {
        "analysis":{
            "tokenizer":{
                "korean_nori_tokenizer":{
                    "type":"nori_tokenizer",
                    "decompound_mode":"mixed",
                }
            },
            "analyzer":{
                "nori_analyzer":{
                    "type":"custom",
                    "tokenizer":"korean_nori_tokenizer",
                    "filter":[
                        "nori_posfilter"    
                    ]
                }
            },
            "filter":{
                "nori_posfilter":{
                    "type":"nori_part_of_speech",
                    "stoptags":[
                        "E",
                        "IC",
                        "J",
                        "MAG",
                        "MM",
                        "NA",
                        "NR",
                        "SC",
                        "SE",
                        "SF",
                        "SH",
                        "SL",
                        "SN",
                        "SP",
                        "SSC",
                        "SSO",
                        "SY",
                        "UNA",
                        "UNKNOWN",
                        "VA",
                        "VCN",
                        "VCP",
                        "VSV",
                        "VV",
                        "VX",
                        "XPN",
                        "XR",
                        "XSA",
                        "XSN",
                        "XSV"
                    ]
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "title": {
                "type": "text",
                "analyzer": "nori_analyzer",
            },
            "content": {
                "type": "text",
                "analyzer": "nori_analyzer",
            },
            "office" : {
                "type" : "keyword"
            },
            "timestamp": {
                "type" : "date",
                "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd'T'HH:mm:ss.SSSZ||epoch_millis"
            },
            "url" : {
                "type" : "keyword"
            },
            "category" : {
                "type" : "keyword"
            },
        }
    }
}

def create_index(body=None):
    
    if not es.indices.exists(index=INDEX):
        return es.indices.create(index=INDEX, body=body)

def insert(naver, daum):
    results = []
    res_set = set()
    cnt = 1
    while True:
        page = requests.get(f"https://sports.news.naver.com/{naver}/news/list?isphoto=N&date={yesterday}&page={cnt}")

        json_list = json.loads(page.content).get('list')

        if (json_list[0].get('oid'), json_list[0].get('aid')) in res_set:
            break

        res_set.add((json_list[0].get('oid'), json_list[0].get('aid')))

        for i in json.loads(page.content).get('list'):
            res = requests.get(f"https://sports.news.naver.com/news?oid={i.get('oid')}&aid={i.get('aid')}")
            res_soup = BeautifulSoup(res.text, 'html.parser')
            datetime_string = i.get('datetime')
            datetime_format = "%Y.%m.%d %H:%M"
            datetime_result = datetime.strptime(datetime_string, datetime_format)
            data = {
                'title' : i.get('title'),
                'content' : res_soup.select('.news_end')[0].text.split('\n')[1],
                'office' : i.get('officeName'),
                'timestamp' : datetime_result.strftime("%Y-%m-%d %H:%M:%S"),
                'url' : f"https://sports.news.naver.com/news?oid={i.get('oid')}&aid={i.get('aid')}",
            }
            results.append(data)
        cnt += 1
    url = f'''https://sports.daum.net/media-api/harmony/contents.json?page=0&consumerType=HARMONY&status=SERVICE&createDt={20230711}000000~{20230711}235959&discoveryTag%5B0%5D=%257B%2522group%2522%253A%2522media%2522%252C%2522key%2522%253A%2522defaultCategoryId3%2522%252C%2522value{daum}&size=20'''
    while True:
        res_d = requests.get(url)

        for i in json.loads(res_d.content).get('result').get('contents'): 
            data = {
                    'title' : i.get('title'),
                    'content' : i.get('bodyText').replace('\n', ' '),
                    'office' : i.get('cp').get('cpName'),
                    'url' : i.get('extra').get('kakaoDomainServiceUrl'),
                    'timestamp' : datetime.utcfromtimestamp(i.get('createDt') // 1000).strftime("%Y-%m-%d %H:%M:%S"),
                    'category' : naver,
                }
            results.append(data)
        if json.loads(res_d.content).get('result').get('hasNext'):
            key = json.loads(res_d.content).get('result').get('contents')[-1].get('searchId')
            k = url.split('&after')
            url = k[0] + f'&after={key}'
        else:
            break
    return results


def run():
    naver = ['wfootball', 'kfootball', 'wbaseball', 'kbaseball', 'basketball']
    daum = ['%2522%253A%2522100032%2522%257D', '%2522%253A%25221027%2522%257D', '%2522%253A%25221015%2522%257D', '%2522%253A%25221028%2522%257D', '%2522%253A%25221029%2522%257D']

    create_index(mappings)


    for n, d in zip(naver, daum):

        data = insert(naver=n, daum=d)

        df = pd.DataFrame(data)

        df['category'] = n

        data = df.to_dict(orient='records')

        docs = [{
          '_index': INDEX,
          '_source': {
              "title": d.get('title'),
              "content": d.get('content'),
              "office": d.get('office'),
              "timestamp": d.get('timestamp'),
              "url":d.get('url'),
              'category':d.get('category')
              }
          } for d in data]
        
        helpers.bulk(es, docs)

        print('save ok')

        

