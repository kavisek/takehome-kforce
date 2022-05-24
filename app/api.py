import pandas as pd
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


def consolidated_dataframe() -> pd.DataFrame:
    """Read consolidate dataframe.

    Returns:
        pd.DataFrame: consolidated dataframe.
    """
    df = pd.read_csv("./output/consolidated_output.1.csv")
    return df


@app.get("/")
def read_root() -> dict:
    """Return full consolidated data

    Request: http://127.0.0.1:8000/

    Returns:
        _type_: dict
    """
    df = consolidated_dataframe()
    json = df.to_json()
    return json


@app.get("/quality/{quality_id}")
def read_quality(quality_id: str) -> dict:
    """Return quality

    Request: http://127.0.0.1:8000/quality/low

    Args:
        quality_id (str): the quality id

    Returns:
        _type_: dict
    """
    df = consolidated_dataframe()
    df = df[df["quality"] == quality_id]
    json = df.to_json()
    return json