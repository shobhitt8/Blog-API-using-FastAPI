# app/routers/dashboard.py

from fastapi import APIRouter, Depends, HTTPException, Query
from app.dependencies.authentication import get_current_user
from app.models.blog import Blog
from pymongo import MongoClient
from dotenv import dotenv_values

router = APIRouter()

config = dotenv_values(".env")

client = MongoClient(config["MONGODB_URI"])
db = client[config["DATABASE_NAME"]]
blogs_collection = db["blogs"]
users_collection = db["users"]

# Fetch all blogs matching user's followed tags (sorted by relevance)
@router.get("/dashboard", response_model=list[Blog])
async def get_user_dashboard(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
    current_user: str = Depends(get_current_user)
):
    # Retrieve user's followed tags
    user_tags = users_collection.find_one({"email": current_user}, {"tags": 1})
    if not user_tags:
        raise HTTPException(status_code=404, detail="User not found")

    followed_tags = user_tags.get("tags", [])
    if not followed_tags:
        raise HTTPException(status_code=400, detail="User has no followed tags")

    # Retrieve blogs matching user's followed tags, sorted by relevance
    blogs = blogs_collection.find(
        {"tags": {"$in": followed_tags}, "author": {"$ne": current_user}}
    ).sort([("tags", -1), ("_id", -1)]).skip(skip).limit(limit)

    return list(blogs)
