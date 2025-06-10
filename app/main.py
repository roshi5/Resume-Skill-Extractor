from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.parser import parse_resume
from app.storage import save_data, get_all_data
import shutil
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, query: str = ""):
    resumes = get_all_data()

    if query:
        query = query.lower()
        resumes = [
            r for r in resumes if
            query in str(r[0]).lower() or  # name
            query in str(r[1]).lower() or  # email
            query in str(r[2]).lower() or  # phone
            query in str(r[3]).lower() or  # skills
            query in str(r[4]).lower()     # experience
        ]

    return templates.TemplateResponse("index.html", {
        "request": request,
        "resumes": resumes,
        "query": query
    })


@app.post("/upload")
async def upload_file(request: Request, file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    data = parse_resume(file_location)
    save_data(data)
    resumes = get_all_data()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "resumes": resumes,
        "skill": "",
        "name": "",
        "email": "",
        "phone": "",
        "experience": ""
    })
