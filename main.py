from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import os
import requests

app = FastAPI()

@app.get("/food")
def get_food_info(name: str = Query(...)):
    # Render 환경변수에서 디코딩된 인증키 불러오기
    service_key = os.getenv("serviceKey")

    if not service_key:
        return JSONResponse(status_code=500, content={"error": "Missing serviceKey"})

    url = "https://apis.data.go.kr/1471000/FoodNtrCpntDbInfo02/getFoodNtrCpntDbInq02"
    params = {
        "desc_kor": name,
        "serviceKey": service_key,
        "type": "json",
        "numOfRows": 5
    }

    try:
        res = requests.get(url, params=params)
        res.raise_for_status()
        data = res.json()

        items = data.get("body", {}).get("items", [])
        if not items:
            return JSONResponse(status_code=404, content={"message": "No data found"})

        return {"food": name, "nutrients": items}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
