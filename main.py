from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from extractor import ExtractFeatures
import pandas as pd
import pickle
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Mount the static folder to serve CSS files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/submit", response_class=HTMLResponse)
async def submit_form(request: Request):
    form_data = await request.form()
    extractor = ExtractFeatures()
    extracted_features = extractor.url_to_features(form_data["url"])
    dataframe = pd.DataFrame(extracted_features, index=[0])
    with open('phishing_url_detector.pkl', 'rb') as file:
        loaded_model = pickle.load(file)
    prediction = loaded_model.predict(dataframe)
    print(prediction)
    return templates.TemplateResponse("result.html", {"request": request})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="8000")