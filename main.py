from app.api.routes import schedules
from app.api.routes import users
from app.api.routes import dashboard
from app.api.routes import cults
from app.api.routes import reports
from app.api.routes import departments
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuração do CORS
origins = [
    "http://localhost:3000", # Frontend rodando localmente no React/Next.js
    "http://localhost:5173", # Frontend rodando no Vite (caso use)
    # Adicione outros domínios aqui quando for para produção (ex: "https://meusite.com")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(schedules.router)
app.include_router(dashboard.router)
app.include_router(cults.router)
app.include_router(reports.router)
app.include_router(departments.router)

@app.get("/")
async def root():
    return {"status": "OK"}