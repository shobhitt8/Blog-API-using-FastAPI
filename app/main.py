# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

app = FastAPI()

# Load environment variables from .env
load_dotenv()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
from app.routers import auth, blogs, dashboard
app.include_router(auth.router)
app.include_router(blogs.router)
app.include_router(dashboard.router)  # Add the dashboard router
