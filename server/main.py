from src.app import app


if __name__ == '__main__':
    from uvicorn import run as uvicorn_run
    
    uvicorn_run(app, host="0.0.0.0", port=8000)
