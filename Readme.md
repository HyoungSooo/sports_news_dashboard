# 네이버 해외축구 뉴스 크롤러 파이프라인
네이버 해외축구 뉴스를 크롤링해서 엘라스틱 서치에 저장하는 파이프라인입니다.

### how to use
```shell
docker-compose up

go to -> 127.0.0.1:8888

copy pipeline.ipynb to jupyter server
```

### Versions
* python==3.9.8
* elasticsearch==7.10.1
* beautifulsoup4==4.4.0

### 네이버 뉴스 클로링 파이프라인
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
            "section": {
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


### 다른 뉴스 클롤링 확장하기
네이버 뉴스의 api 호출 경로는 다음과 같습니다
```shell
https://sports.news.naver.com/<category>/news/list?isphoto=N

# 해외축구
https://sports.news.naver.com/wfootball/news/list?isphoto=N

# 해외 야구
https://sports.news.naver.com/wbaseball/news/list?isphoto=N

```
<category>부분을 수정하여 여러 다른 뉴스도 수집 할 수 있습니다.

크롤링에 필요한 쿼리 파라미터는 다음과 같습니다

```shell
https://sports.news.naver.com/wfootball/news/list?isphoto=N&date={today}&page={cnt}

date: int
page: int

```
네이버 뉴스 최신뉴스 탭 기준임으로 다른 탭의 뉴스의 api는 다를 수 있습니다.

page파라미터는 가장 마지막 페이지의 숫자를 기준으로 그 이상의 숫자는 항상 마지막 페이지의 데이터를 가져오게 됩니다.

```python
if (json_list[0].get('oid'), json_list[0].get('aid')) in res_set:
    break
```

### future works
* crontab을 활용하여 매일 정해진 시각에 뉴스를 크롤링하는 기능
* 간단한 챗봇을 만들어 사용자가 입력하는 키워드에 맞는 뉴스를 제공
