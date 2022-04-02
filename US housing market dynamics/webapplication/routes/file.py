
from fastapi import APIRouter,Request,Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pymongo import MongoClient

client = MongoClient("mongodb+srv://sanjay:1234@cluster0.gxmvm.mongodb.net/US_Housing?retryWrites=true&w=majority")
dbs = client["US_Housing"]

 

dashboard=APIRouter()
templates=Jinja2Templates(directory="html")

@dashboard.get("/",response_class=HTMLResponse)
def chart(request: Request):
    global dbs
    db = dbs["Metric_Analysis"]
    select3="Brevard County, FL"
    select2="county"
    select1="median_sale_price"
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
    return templates.TemplateResponse("index.html",{"request":request,"x":x,"y":y,"select1":select1,"select2":select2,"select3":select3})

@dashboard.post("/")
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
    
@dashboard.get("/price")
async def metric_name(request: Request):
    global dbs
    db = dbs["Price_Drops"]
    select3="Brevard County, FL"
    select2="county"
    select1="total_homes_sold_with_price_drops"
    metricaggregate=db.aggregate([{
    "$group" : 
        {"_id" : {
            "region_name": "$"+select3,
            "region_type": "$"+select2,
            "Quartile": "$Quartile",

        }, 
        
         "price_avg" : { "$avg" : "$"+select1 }
         }},
    ])
    # metricaggregate=db.find({"region_name": select1,"region_type": select2})
    x=[]
    y=[]
    for aggregate in metricaggregate:
        q=str(aggregate['_id']['Quartile'])
        x.append(q)
        y.append(aggregate['price_avg'])
    
    print(x)
    print(y)
    return templates.TemplateResponse("pricing.html",{"request":request,"x":x,"y":y,"select1":select1,"select2":select2,"select3":select3})


@dashboard.post("/price")
async def metric_name(request: Request,select1: str = Form(...),select2: str = Form(...),select3: str = Form(...)):
    global dbs
    db = dbs["Price_Drops"]
    print(select1,select2,select3)
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

    return templates.TemplateResponse("pricing.html",{"request":request,"x":x,"y":y,"select1":select1,"select2":select2,"select3":select3})