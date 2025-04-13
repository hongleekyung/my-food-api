import os
import urllib.parse
import requests
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/food")
def get_food_info(name: str = Query(..., alias="name")):
    raw_key = os.getenv("serviceKey")

    if not raw_key:
        return JSONResponse(status_code=500, content={"error": "Missing serviceKey"})

    encoded_key = urllib.parse.quote(raw_key, safe='')  # ← 인코딩 필수!

    url = "https://apis.data.go.kr/1471000/FoodNtrCpntDbInfo02/getFoodNtrCpntDbInq02"
    params = {
        "serviceKey": encoded_key,
        "desc_kor": name,
        "numOfRows": 5,
        "type": "json"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        items = data.get("body", {}).get("items", [])
        if not items:
            return JSONResponse(status_code=404, content={"message": "No data found"})

        return {"food": name, "nutrients": items}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
