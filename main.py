import os
import requests
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/food")
def get_food_info(name: str = Query(...)):
    service_key = os.getenv("serviceKey")  # 디코딩된 키가 환경변수에 저장되어 있다고 가정

    if not service_key:
        return JSONResponse(status_code=500, content={"error": "Missing serviceKey"})

    url = "https://apis.data.go.kr/1471000/FoodNtrCpntDbInfo02/getFoodNtrCpntDbInq02"
    params = {
        "serviceKey": service_key,  # 이건 디코딩된 상태여야 함
        "desc_kor": name,
        "numOfRows": 5,
        "type": "json"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        items = data.get("body", {}).get("items", [])
        if not items:
            return JSONResponse(status_code=404, content={"message": "No data found"})

        return {"food": name, "nutrients": items}
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
