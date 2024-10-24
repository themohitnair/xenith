import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager

from routers.author import author_router
from routers.book import book_router
from routers.borrow import borrow_router
from routers.copy import copy_router
from routers.genre import genre_router
from routers.librarian import librarian_router
from routers.library import library_router
from routers.patron import patron_router
from routers.publisher import publisher_router
from routers.writes import writes_router

from database import init_db

def setup_logging():
    logger = logging.getLogger()
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        
        file_handler = logging.FileHandler('app.log')
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter('[ %(levelname)s: %(asctime)s ] - %(message)s')
        file_handler.setFormatter(file_formatter)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('%(levelname)s:\t  %(message)s')
        console_handler.setFormatter(console_formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    # await init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(router=author_router, prefix="/author")
app.include_router(router=book_router, prefix="/book")
app.include_router(router=borrow_router, prefix="/borrow")
app.include_router(router=copy_router, prefix="/copy")
app.include_router(router=librarian_router, prefix="/librarian")
app.include_router(router=library_router, prefix="/library")
app.include_router(router=patron_router, prefix="/patron")
app.include_router(router=publisher_router, prefix="/publisher")


    

@app.get("/")
def greet():
    return {
        "app": "Xenith",
        "desc": "Library Management made easy"
    }

@app.get("/dashboard")
def dashboard():
    return {
        "message": "This is the dashboard"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(port=8000, host="127.0.0.1", reload=True, app="main:app")