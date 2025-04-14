from fastapi import FastAPI, HTTPException, Request
import uvicorn
from routes import auth, balance, Model
from database.database import init_db

app = FastAPI()
app.include_router(auth.router, tags=['auth'], prefix='/auth')
app.include_router(balance.router, tags=['balance'], prefix='/balance')
app.include_router(Model.router, tags=['Model'], prefix='/Model')

init_db()


@app.get("/")
async def root():
    return {"message": "Welcome to the ML Prediction Service API"}

if __name__ == "__main__":
    uvicorn.run('api:app', host='0.0.0.0', port=8080, reload=True)
