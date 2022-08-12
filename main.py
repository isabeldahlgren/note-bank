from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from converter import converter
import markdown
import os


app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def load_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/{file_path:path}", response_class=HTMLResponse)
async def load_module(file_path: str, request: Request):
    field = file_path.split("/")[0]
    files = [file for file in os.listdir(f"./{field}") if file[-4:] == ".tex"]
    topics = [file[:-4] for file in files]
    if not "/" in file_path:
        description = str()
        with open(os.path.join(f"./{field}", "description.md")) as file:
            description += markdown.markdown(file.read())
        return templates.TemplateResponse("field.html", {"request": request, "field": field, "description": description, "topics": topics})
    else:
        module = file_path.split("/")[1]
        path = f"./{field}/{module}.tex"
        content = converter(path)
        return templates.TemplateResponse("module.html", {"request": request, "field": field, "topics": topics, "content": content})