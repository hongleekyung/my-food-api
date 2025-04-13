from fastapi import FastAPI, Query
import requests
from fastapi.responses import JSONResponse
import urllib.parse

app = FastAPI()

# 인코딩된 serviceKey (꼭 본인 걸로 바꿔주세요)
SERVICE_KEY = "5Q70tsGRHEhW1gdaElpBNoKkspmHxZZO9rsEwkBNq4kXx%2B5lyGHevhvgK06eor4X%2FeKg5REWVbXjXVAKmYKshQ%3D%3D"

@app.get("/food")
def get_food_info(name: str = Query(..., alias="name")):
    encoded_name = urllib.parse.quote(name)
    url = f"https://apis.data.go.kr/1471000/FoodNtrCpntDbInfo02/getFoodNtrCpntDbInq02"
    
    params = {
        "serviceKey": SERVICE_KEY,
        "desc_kor": encoded_name,
        "numOfRows": 5,
        "type": "json"
    }

    response = requests.get(url, params=params)
    data = response.json()

    # 간단히 items만 추려서 반환
    items = data.get("body", {}).get("items", [])
    return JSONResponse(content=items)
