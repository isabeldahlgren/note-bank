from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from converter import converter
import os

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def load_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


""" @app.get("/{path}", response_class=HTMLResponse)
async def load_field(path: str, request: Request):
    print("In basic func!")
    files = [file for file in os.listdir(f'./{path}') if file[-4:] == ".tex"]
    topics = [file[:-4].capitalize() for file in files]
    return templates.TemplateResponse("field.html", {"request": request, "field": path.capitalize(), "topics": topics})
 """

@app.get("/{file_path:path}", response_class=HTMLResponse)
async def load_module(file_path: str, request: Request):
    delimiter = '/'
    field = file_path.split(delimiter)[0].capitalize()
    files = [file for file in os.listdir(f'./{field}') if file[-4:] == ".tex"]
    topics = [file[:-4].capitalize() for file in files]
    if not delimiter in file_path:
        return templates.TemplateResponse("field.html", {"request": request, "field": field, "topics": topics})
    else:
        module = file_path.split(delimiter)[1]
        path = f'./{field}/{module}.tex'
        content = converter(path)
        return templates.TemplateResponse("module.html", {"request": request, "field": field, "topics": topics, "content": content})