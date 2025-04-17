from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from routes import user, balance, Model, home, login
from database.database import init_db
from database.config import get_settings

settings = get_settings()

app = FastAPI()
app.include_router(login.router, tags=['login'], prefix='/login')
app.include_router(user.router, tags=['users'], prefix='/api/users')
app.include_router(balance.router, tags=['balance'], prefix='/api/balance')
app.include_router(Model.router, tags=['Model'], prefix='/api/model')
app.include_router(home.router, tags=['home'])

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()


if __name__ == "__main__":
    uvicorn.run('api:app', host='0.0.0.0', port=8080, reload=True)
