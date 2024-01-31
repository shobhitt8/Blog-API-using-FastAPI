from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies.authentication import get_current_user
from app.models.user import User, UserCreate, UserUpdate
from pymongo import MongoClient
from dotenv import dotenv_values

router = APIRouter()

config = dotenv_values(".env")

client = MongoClient(config["MONGODB_URI"])
db = client[config["DATABASE_NAME"]]
users_collection = db["users"]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Register new users
@router.post("/register", response_model=User)
async def register(user: UserCreate):
    # Check if user already exists
    existing_user = users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )
    
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())

   # Create a new user document in the database
    new_user = {
        "email": user.email,
        "password": hashed_password,
        "tags": [],
    }
    result = users_collection.insert_one(new_user)
    new_user["_id"] = str(result.inserted_id)

    return new_user

# Login existing users
@router.post("/login", response_model=User)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Find the user in the database
    user = users_collection.find_one({"email": form_data.username})
    if not user or user["password"] != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate a new access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user["email"]}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}

# Update user profile
@router.put("/profile", response_model=User)
async def update_profile(user_update: UserUpdate, current_user: str = Depends(get_current_user)):
    # Update user tags in the database
    result = users_collection.update_one({"email": current_user}, {"$set": {"tags": user_update.tags}})
    
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    # Retrieve the updated user
    updated_user = users_collection.find_one({"email": current_user})
    
    return updated_user

# Add/remove user tags
@router.put("/tags", response_model=User)
async def update_tags(tags: List[str], current_user: str = Depends(get_current_user)):
    # Update user tags in the database
    result = users_collection.update_one({"email": current_user}, {"$set": {"tags": tags}})
    
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    # Retrieve the updated user
    updated_user = users_collection.find_one({"email": current_user})
    
    return updated_user  
