# Simple main.py that imports and runs the simple version
from main_simple import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
