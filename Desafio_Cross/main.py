from config import list_num
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def numeros():
    return {"numbers": list_num}

