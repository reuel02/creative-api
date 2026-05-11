from app.api.routes import schedules
from app.api.routes import users
from fastapi import FastAPI

app = FastAPI()

app.include_router(users.router)
app.include_router(schedules.router)

@app.get("/")
async def root():
    return {"status": "OK"}