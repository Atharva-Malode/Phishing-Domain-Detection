from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from extractor import ExtractFeatures
from pycaret.classification import setup, predict_model
import pandas as pd
import pickle

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Mount the static folder to serve CSS files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load the trained model using pickle
with open('xgb.pkl', 'rb') as file:
    loaded_tuned_model = pickle.load(file)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/submit", response_class=HTMLResponse)
async def submit_form(request: Request):
    form_data = await request.form()
    extractor = ExtractFeatures()
    url = form_data["url"]
    features = extractor.url_to_features(url)
    dataframe = pd.DataFrame([features])
    predictions = loaded_tuned_model.predict(dataframe)
    print(predictions)
    if predictions[0] == 0:
        return templates.TemplateResponse("result.html", {"request": request, "url": form_data["url"], "prediction": "Not Phishing"})
    return templates.TemplateResponse("result.html", {"request": request, "url": form_data["url"], "prediction": "Phishing"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="8000")