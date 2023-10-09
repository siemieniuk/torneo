# import auth
# import model as _model

# import tournament
import uvicorn
from api.v1.router import api_router as v1_router
from core.database import Base, engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


class AppCreator:
    def __init__(self):
        self.app = FastAPI()


app = FastAPI()

Base.metadata.create_all(bind=engine)

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(auth.router, prefix="/auth", tags=["auth"])
# app.include_router(tournament.router, prefix="/tournament", tags=["tournament"])

app.include_router(v1_router, prefix="/api/v1", tags=["auth"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
