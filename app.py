import sys
import os
import json

from Network_Security.Exception.exception import NetworkSecurityException
from Network_Security.Logging.logger import logging
from Network_Security.Pipeline.training_pipeline import TrainingPipeline 

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd

# Removed pymongo code and added json file reading
from Network_Security.Constants.Training_Pipeline import (
    DATA_INGESTION_COLLECTION_NAME, 
    DATA_INGESTION_DATABASE_NAME
)
from Network_Security.Utils.main_utils.utils import load_object
from Network_Security.Utils.ml_utils.model.estimator import NetworkModel

def load_data_from_json(file_path):
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
        return data
    except Exception as e:
        raise NetworkSecurityException(f"Error loading JSON file: {str(e)}", sys)

# Replace the MongoDB connection with loading data from local JSON file
file_path =  "HIMANSHU_AI.json" # Adjust the path to your JSON file
data = load_data_from_json(file_path)  # Loading data from local JSON

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful")
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        # Load preprocessor and final model from pickle files
        preprocessor = load_object("final_model/preprocessor.pkl")
        final_model = load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocessor=preprocessor, model=final_model)

        # Print first row for inspection (this is optional, you might want to remove it in production)
        print(df.iloc[0])

        # Make predictions using the loaded model
        y_pred = network_model.predict(df)
        print(y_pred)

        # Add predicted column to dataframe
        df['predicted_column'] = y_pred
        print(df['predicted_column'])

        # Save the output to a CSV file (consider adjusting this based on your use case)
        df.to_csv('prediction_output/output.csv')

        # Convert DataFrame to HTML table for display
        table_html = df.to_html(classes='table table-striped')

        # Return the rendered HTML table in response
        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})
        
    except Exception as e:
        raise NetworkSecurityException(e, sys)

if __name__ == "__main__":
    app_run(app, host="0.0.0.0", port=8000)
