from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Mount the static folder to serve CSS files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/submit", response_class=HTMLResponse)
async def submit_form(request: Request):
    # Process the form submission here
    # You can use the 'answer' variable to get the submitted value from the form

    # For now, let's assume you want to display the submitted answer in 'result.html'
    return templates.TemplateResponse("result.html", {"request": request})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="8000")