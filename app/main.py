from typing import List
from database.db import *
from fastapi import FastAPI
from pydantic import BaseModel



app = FastAPI()




@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

