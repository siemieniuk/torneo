import uvicorn
from backend.database import Base, engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def home():
    return {"message": "Welcome to Torneo!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
