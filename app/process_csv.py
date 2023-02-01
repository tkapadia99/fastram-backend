import pandas as pd

import os
from dotenv import load_dotenv
from azure.cosmos import CosmosClient
import numpy as np


load_dotenv()

endpoint = os.environ["ENDPOINT"]
primary_key = os.environ["PRIMARY_KEY"]

client = CosmosClient(url=endpoint, credential=primary_key).get_database_client(database="FastramDB")

strong = client.get_container_client("strongdata")

#queries all existing data
items = list(strong.query_items(query="select * from strongdata", enable_cross_partition_query=True))

print("Deleting Data \n")

#deletes all items in DB
for item in items:
    strong.delete_item(item, partition_key=item["id"])

print("Inserting New Data \n")

#reads in new data
df = pd.read_csv('../strong.csv')

#converts headers to snake case
df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(" ", "_")

#replaces pandas nan
df = df.replace({np.nan: None})

#converts to objects
records = df.to_dict(orient="records")


for record in records:
    strong.create_item(body=record, enable_automatic_id_generation=True)


print("Inserted {} New Records!".format(len(records)))