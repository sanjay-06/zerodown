from fastapi import FastAPI
from routes.file import dashboard
from fastapi.staticfiles import StaticFiles
import uvicorn

app=FastAPI()

app.mount("/static", StaticFiles(directory="html/css"), name="static")

app.include_router(dashboard)

uvicorn.run(app,host='0.0.0.0',port=8000)