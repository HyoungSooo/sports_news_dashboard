# 스포츠 뉴스 크롤링 대시보드
네이버 해외축구 뉴스를 크롤링해서 엘라스틱 서치에 저장하는 파이프라인입니다.

### how to use
```shell
docker-compose up --env-file .env up --build

go to -> 127.0.0.1:5085
```
### 스포츠 뉴스 크롤링 대시보드
현재 날짜 기준 어제의 날짜에 게시된 뉴스 전체를 크롤링합니다.

elastcisearch index mapping
```python
from elasticsearch import Elasticsearch
# defualt mappings in elasticsearch
# you can change to fit your database

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
            "category": {
                "type" : "keyword"
            }
        }
    }
}

```
토크나이저는 노리를 사용합니다.
노리 토크나이저는 도커에 기본 설치되어있지 않음으로 엘라스틱 서치 도커 컨테이너 내에서 설치 해줘야 합니다
```shell
cd /usr/share/elasticsearch/bin/
./elasticsearch-plugin install analysis-nori
```

### kibana index patterns
http://127.0.0.1:5601 -> stack management -> index patterns -> create index pattern

### kibana discover result
![image](https://github.com/HyoungSooo/sample_web_store_api/assets/86239441/b9e29fc0-5853-48f9-b4ee-18cdfd2fbdcf)


### 대시보드

#### 인덱스 화면
![화면 캡처 2023-07-14 145742](https://github.com/HyoungSooo/sports_news_dashboard/assets/86239441/dcad9ac3-92e1-414a-9347-99e73e53bb49)

#### 검색 기능 제공
![화면 캡처 2023-07-14 150405](https://github.com/HyoungSooo/sports_news_dashboard/assets/86239441/b3ea41e0-4357-46bd-afa7-7c4f43aae0d6)

![화면 캡처 2023-07-14 150416](https://github.com/HyoungSooo/sports_news_dashboard/assets/86239441/78ecdc92-3361-4bf9-9dfb-00bf12f156a0)


### 구조도
![image](https://github.com/HyoungSooo/sports_news_dashboard/assets/86239441/43f526f4-b54b-40c5-b60c-2386d2cc1568)


