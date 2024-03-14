from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse, Response

from .models import AddKeyValuePairRequest, UpdateKeyValuePairRequest
from .redis_client import redis_client
from .tasks import delete_key_value_pair, set_key_value_pair
from .templating import get_template_path


app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def get_homepage():
    return FileResponse(get_template_path("homepage.html"))


@app.get("/api/data/get/{key}")
def get_key_value_pair_api(key: str):
    value = redis_client.get(key)

    if value is None:
        return JSONResponse(status_code=404, content={
            'success': False,
            'error': {
                'message': "Key does not exist.",
            },
        })
    
    return JSONResponse(status_code=200, content={
        'success': True,
        'result': {
            'key': key,
            'value': value,
        },
    })


@app.post("/api/data/add")
async def add_key_value_pair_api(data: AddKeyValuePairRequest):
    if redis_client.exists(data.key):
        return JSONResponse(status_code=400, content={
            'success': False,
            'error': {
                'message': "Key already exists",
            },
        })
    
    set_key_value_pair(data.key, data.value)

    return JSONResponse(status_code=200, content={
        'success': True,
        'result': {
            'key': data.key,
            'value': data.value,
        },
    })


@app.put("/api/data/update/{key}")
async def set_key_value_pair_api(key: str, data: UpdateKeyValuePairRequest):
    if not redis_client.exists(key):
        return JSONResponse(status_code=404, content={
            'success': False,
            'error': {
                'message': "Key does not exist.",
            },
        })
    
    set_key_value_pair(key, data.value)

    return JSONResponse(status_code=200, content={
        'success': True,
        'result': {
            'key': key,
            'value': data.value,
        },
    })


@app.delete("/api/data/delete/{key}")
async def delete_key_value_pair_api(key: str):
    if not redis_client.exists(key):
        return JSONResponse(status_code=404, content={
            'success': False,
            'error': {
                'message': "Key does not exist.",
            },
        })
    
    delete_key_value_pair(key)

    return Response(status_code=204)
