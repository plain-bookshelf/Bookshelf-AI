from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Reco_System.recommendation_engine import init_if_needed
from Chatbot.main import router as chatbot_router
from Reco_System.main import router as reco_system_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chatbot_router)
app.include_router(reco_system_router)

@app.on_event("startup")
async def _startup():
    init_if_needed()

@app.get("/")
async def root():
    return {"message": "Hello World"}
