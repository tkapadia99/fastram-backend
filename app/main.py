from typing import List
from fastapi import FastAPI
import os
from dotenv import load_dotenv
from azure.cosmos import CosmosClient
from .schema import recordOut, daily_record
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

endpoint = os.environ["ENDPOINT"]
primary_key = os.environ["PRIMARY_KEY"]

client = CosmosClient(url=endpoint, credential=primary_key).get_database_client(database="FastramDB")

strong = client.get_container_client("strongdata")

@app.get("/")
def root():
    return "Welcome to Fastram Backend, see https://fastram-backend.azurewebsites.net/docs"

@app.get("/exercise_types")
def get_all_exercise_types():
    
    types = list(strong.query_items(query="SELECT DISTINCT VALUE c[@field] from c",
        parameters=[{"name":"@field", "value": "exercise_name"}], enable_cross_partition_query=True))

    return types

@app.get("/records", response_model=List[recordOut])
def get_records():

    items = list(strong.query_items(query="select * from strongdata", enable_cross_partition_query=True))

    return items

@app.get("/records/{exercise}", response_model=List[recordOut])
def get_records_by_exercise_type(exercise: str):

    items = list(strong.query_items(query="select * from strongdata where strongdata[@field] = @exname",
        parameters=[{"name": "@exname", "value": exercise}, {"name":"@field", "value": "exercise_name"}], enable_cross_partition_query=True))

    return items

@app.get("/bestdailyrecord/{exercise}")
def get_daily_record_by_exercise_type(exercise: str):

    items = list(strong.query_items(query="select * from strongdata where strongdata[@field] = @exname",
        parameters=[{"name": "@exname", "value": exercise}, {"name":"@field", "value": "exercise_name"}], enable_cross_partition_query=True))

    df = pd.DataFrame(data = items)

    df = df.groupby("date")["weight"].apply(list).apply(lambda x: max(x))

    obj = {"dates": list(df.index.values),
            "best_weight": list(df.values)}

    return obj