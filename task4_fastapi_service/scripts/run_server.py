"""Script to start the FastAPI server with Uvicorn."""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import uvicorn

from config.settings import APP_HOST, APP_PORT

if __name__ == "__main__":
    uvicorn.run("src.app:app", host=APP_HOST, port=APP_PORT, reload=True)
