
from fastapi import APIRouter,Request,Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from numpy import select
from pymongo import MongoClient
from pprint import pprint
client = MongoClient("mongodb+srv://sanjay:1234@cluster0.gxmvm.mongodb.net/US_Housing?retryWrites=true&w=majority")
dbs = client["US_Housing"]

 

dashboard=APIRouter()
templates=Jinja2Templates(directory="html")

@dashboard.get("/",response_class=HTMLResponse)
def chart(request: Request):
    global dbs
    db = dbs["Metric_Analysis"]
    select1="Brevard County, FL"
    select2="county"
    select3="median_sale_price"
    metricaggregate=db.aggregate([{
    "$group" : 
        {"_id" : {
            "region_name": "$"+select1,
            "region_type": "$"+select2,
            "Quartile": "$Quartile",

        }, 
        
         "metric_avg" : { "$avg" : "$"+select3 }
         }},
    ])
    x=[]
    y=[]
    for aggregate in metricaggregate:
        q=str(aggregate['_id']['Quartile'])
        x.append(q)
        y.append(aggregate['metric_avg'])
    return templates.TemplateResponse("index.html",{"request":request,"x":x,"y":y,"select1":select1,"select2":select2,"select3":select3})

@dashboard.post("/metric")
async def metric_name(request: Request,select1: str = Form(...),select2: str = Form(...),select3: str = Form(...)):
    global dbs
    db = dbs["Metric_Analysis"]
    metricaggregate=db.aggregate([{
    "$group" : 
        {"_id" : {
            "region_name": "$"+select3,
            "region_type": "$"+select2,
            "Quartile": "$Quartile",

        }, 
        
         "metric_avg" : { "$avg" : "$"+select1 }
         }},
    ])
    x=[]
    y=[]
    for aggregate in metricaggregate:
        q=str(aggregate['_id']['Quartile'])
        x.append(q)
        y.append(aggregate['metric_avg'])
    
    print(x)
    print(y)

    return templates.TemplateResponse("index.html",{"request":request,"x":x,"y":y,"select1":select1,"select2":select2,"select3":select3})
    
# @dashboard.post("/region")
# async def metric_name(request: Request,):
#    print(select2)
#    return templates.TemplateResponse("index.html",{"request":request,"data":"hello1"})