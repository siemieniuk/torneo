from sqlite3 import IntegrityError

import uvicorn
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from api.v1.router import api_router as v1_router
from core.container import Container
from core.database import Base


class AppCreator:
    def __init__(self):
        self.app = FastAPI()

        # Add pagination
        add_pagination(self.app)

        # Configure database
        self.container = Container()
        self.db = self.container.db
        # self.db().create_database()

        # Configure middleware
        origins = ["http://localhost:3000"]
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Include routers
        self.app.include_router(v1_router, prefix="/api/v1")


app_creator = AppCreator()
app = app_creator.app

db = app_creator.db
container = app_creator.container


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
