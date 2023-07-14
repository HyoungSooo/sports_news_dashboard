from django.urls import re_path, path
from django.views.decorators.csrf import csrf_exempt

from api.views import *

from ninja import Router, NinjaAPI
from ninja.schema import Schema
from typing import List
from home.models import Product, DefaultDate, WordCloud

from datetime import datetime

from pipeline.crawler import run
from datetime import datetime, timedelta
from elasticsearch import Elasticsearch, helpers

delta = timedelta(days=1)
yesterday = datetime.now() - delta + timedelta(hours=9)
ymd = yesterday.strftime("%Y%m%d")
ymd_format = yesterday.strftime("%Y-%m-%d")
INDEX = f'news_{ymd}'

es = Elasticsearch('http://elasticsearch:9200')

api = NinjaAPI()

class ProductSchema(Schema):
    title: str
    content: str
    url: str
    office: str
    timestamp: str
    category: str

class WordCloud(Schema):
    string: str
    count: int
    category: str


@api.post("/products/bulk-create")
def bulk_create_products(request, items: List[ProductSchema]):
    
    now = DefaultDate.objects.get_or_create(date=ymd)[0]

    created_products = []
    for item in items:
        product = Product(**item.dict(), date = now)
        created_products.append(product)
    
    Product.objects.bulk_create(created_products)
    
    return {"message": "Products created successfully"}

@api.post("/words/bulk-create")
def bulk_create_products(request, items: List[WordCloud]):
    
    now = DefaultDate.objects.get_or_create(date=ymd)[0]

    created_products = []
    for item in items:
        product = WordCloud(**item.dict(), date = now)
        created_products.append(product)
    
    WordCloud.objects.bulk_create(created_products)
    
    return {"message": "Products created successfully"}

@api.get('/crawling')
def run_pipeline(request):
    tdy = DefaultDate.objects.get_or_create(date= ymd_format)[0]
    if tdy.crawl:
        return
    else:
        run()
        tdy.crawl = True
        tdy.save()
    return 

@api.get('/pipeline/es')
def get_es_data_to_postgres(request):
    tdy = DefaultDate.objects.get_or_create(date= ymd_format)[0]

    if tdy.sync:
        return
    else:
        results_today = es.search(index=f'news_{ymd}', body={'from':0, 'size':10000, 'query':{'match_all':{}}})
        ps = [Product(**i.get('_source'), date = tdy) for i in results_today.get('hits').get('hits')]

        Product.objects.bulk_create(ps,batch_size=100)

        tdy.sync = True
        tdy.save()
        print('ok')
        return

@api.get('/es')
def search_results(request,q:str):
    results = es.search(index=f'news_{ymd}', body={'from':0, 'size':30, 'query':{'match':{'content':q}}})
    return results.get('hits').get('hits')

urlpatterns = [

	re_path("product/((?P<pk>\d+)/)?", csrf_exempt(ProductView.as_view())),
  path("", api.urls)
]