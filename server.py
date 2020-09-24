import datetime
from dateutil import parser
import json
import typing
from dataclasses import dataclass

import tinydb
from fastapi.encoders import jsonable_encoder
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel


class Measurement(BaseModel):
    string: datetime.datetime
    results: typing.List[dict]
    questionnaire: dict
    id: str


app = FastAPI()

db = tinydb.TinyDB("tiny.db")


@app.get("/")
def root() -> typing.List[Measurement]:
    return db.all()


@app.post("/insert")
def insert(measurement: typing.Dict): #typing.List[Measurement]):
    qu = tinydb.Query()
    json_compatible_item_data = jsonable_encoder(measurement)
    if(len(db.search(qu.timeStamp == measurement["timeStamp"])) == 0):
        db.insert(json_compatible_item_data)
    else:
        db.update(json_compatible_item_data, qu.timeStamp == measurement["timeStamp"])


@app.get("/latest")
def latest(userId: str) -> str:
    qu = tinydb.Query()
    result = db.get(qu.id == userId, len(db))
    if result is not None:
        return parser.parse(result["timeStamp"]).strftime("%Y-%m-%dT%H:%M:%SZ")
    else:
        return datetime.datetime(1970, 1, 1).strftime("%Y-%m-%dT%H:%M:%SZ")


def run():
    uvicorn.run(app, host="0.0.0.0", port=8090)


run()

