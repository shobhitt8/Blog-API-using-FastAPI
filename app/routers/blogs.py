# app/routers/blogs.py

from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.dependencies.authentication import get_current_user
from app.models.blog import Blog, BlogCreate, BlogUpdate
from pymongo import MongoClient
from dotenv import dotenv_values

router = APIRouter()

config = dotenv_values(".env")

client = MongoClient(config["MONGODB_URI"])
db = client[config["DATABASE_NAME"]]
blogs_collection = db["blogs"]

# Create new blogs
@router.post("/blogs", response_model=Blog)
async def create_blog(blog_create: BlogCreate, current_user: str = Depends(get_current_user)):
    blog_data = blog_create.dict()
    blog_data["tags"] = list(set(blog_data["tags"]))  # Ensure unique tags
    blog_data["author"] = current_user
    result = blogs_collection.insert_one(blog_data)
    blog_data["_id"] = str(result.inserted_id)
    return blog_data

# Retrieve all blogs with pagination
@router.get("/blogs", response_model=list[Blog])
async def get_all_blogs(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
    current_user: str = Depends(get_current_user)
):
    blogs = blogs_collection.find().skip(skip).limit(limit)
    return list(blogs)

# Retrieve a specific blog by ID
@router.get("/blogs/{blog_id}", response_model=Blog)
async def get_blog_by_id(blog_id: str):
    blog = blogs_collection.find_one({"_id": blog_id})
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    return blog

# Update existing blogs
@router.put("/blogs/{blog_id}", response_model=Blog)
async def update_blog(blog_id: str, blog_update: BlogUpdate, current_user: str = Depends(get_current_user)):
    # Check if the blog exists
    existing_blog = blogs_collection.find_one({"_id": blog_id, "author": current_user})
    if not existing_blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")

    # Update the blog data
    updated_data = {k: v for k, v in blog_update.dict().items() if v is not None}
    updated_data["tags"] = list(set(updated_data.get("tags", [])))  # Ensure unique tags

    result = blogs_collection.update_one({"_id": blog_id}, {"$set": updated_data})
    
    if result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")

    # Retrieve the updated blog
    updated_blog = blogs_collection.find_one({"_id": blog_id})
    
    return updated_blog

# Delete blogs
@router.delete("/blogs/{blog_id}", response_model=dict)
async def delete_blog(blog_id: str, current_user: str = Depends(get_current_user)):
    # Check if the blog exists
    existing_blog = blogs_collection.find_one({"_id": blog_id, "author": current_user})
    if not existing_blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")

    # Delete the blog
    result = blogs_collection.delete_one({"_id": blog_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")

    return {"message": "Blog deleted successfully"}
