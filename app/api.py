import pandas as pd
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


def consolidated_dataframe():
    """Read consolidate data"""
    df = pd.read_csv("./output/consolidated_output.1.csv")
    return df


@app.get("/")
def read_root():
    """Root: http://127.0.0.1:8000/"""
    df = consolidated_dataframe()
    json = df.to_json()
    return json


@app.get("/quality/{quality_id}")
def read_quality(quality_id: str):
    """Return quality

    Request: http://127.0.0.1:8000/quality/low

    Args:
        quality_id (str): _description_

    Returns:
        _type_: _description_
    """
    df = consolidated_dataframe()
    df = df[df["quality"] == quality_id]
    json = df.to_json()
    return json