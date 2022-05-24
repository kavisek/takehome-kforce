import pandas as pd
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def read_root():
    df = pd.read_csv("./output/consolidated_output.1.csv", index_col=False)
    json = df.to_json()
    return json