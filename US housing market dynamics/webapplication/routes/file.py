
from ast import For
from fastapi import APIRouter,Request,Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import List

dashboard=APIRouter()
templates=Jinja2Templates(directory="html")

@dashboard.get("/",response_class=HTMLResponse)
def chart(request: Request):
    return templates.TemplateResponse("index.html",{"request":request,"data":""})

@dashboard.post("/metric")
async def metric_name(request: Request,select: str = Form(...)):
    return templates.TemplateResponse("index.html",{"request":request,"data":"hello"})
    
@dashboard.post("/region")
async def metric_name(request: Request,select2: str = Form(...)):
   print(select2)
   return templates.TemplateResponse("index.html",{"request":request,"data":"hello1"})