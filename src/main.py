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

@app.get("/{page}", response_class=HTMLResponse)
async def load_module(page, request: Request):
    files = [file for file in os.listdir(f'./{page}') if file[-4:] == ".tex"]
    paths = [os.path.join(f'./{page}', file) for file in files]
    topics = [file[:-4] for file in files]
    content = converter(paths)
    print(content)
    return templates.TemplateResponse("module.html", {"request": request, "content": content, "topics": topics})