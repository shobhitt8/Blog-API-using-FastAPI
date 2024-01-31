
# Blog API with FastAPI Project

## Introduction

This project is a simple FastAPI-based RESTful API for managing a blog. It includes user authentication, blog CRUD operations, and a dashboard feature that fetches blogs based on user-followed tags.

## Technology Stack

- Python
- FastAPI
- Pydantic
- MongoDB
- Docker

## Project Objectives

- Demonstrate proficiency in building RESTful APIs with FastAPI.
- Implement user authentication and authorization using JWT.
- Manage CRUD (Create, Read, Update, Delete) operations for blog data.
- Implement pagination and sorting of blog content.
- Follow best practices for code structure and API architecture.

## API Endpoints

### Authentication:

- Register new users
- Login existing users
- Update user profiles
- Add/remove user tags (keywords or their interests like coding, photography, etc.)

### Blogs:

- Create new blogs
- Retrieve all blogs (with pagination)
- Retrieve a specific blog by ID
- Update existing blogs
- Delete blogs

### Dashboard:

- Fetch all blogs matching user's followed tags (sorted by relevance)
- Implement sorting logic to prioritize blogs with tags the user likes.
- Implement pagination.

## Deployment

The API is Dockerized and can be deployed to a free hosting platform like [render.com](https://render.com).

## Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/your-repository.git

2.Install dependencies:

pip install -r requirements.txt

Set up a MongoDB instance and update the .env file with the MongoDB URI.

3.Build and run the Docker container:

docker build -t my-fastapi-app .
docker run -p 8080:80 --name my-fastapi-container my-fastapi-app
Access the API at http://localhost:8080/docs for interactive documentation.

## Project Structure
project-root/
|-- app/
|   |-- __init__.py
|   |-- main.py
|   |-- models/
|       |-- __init__.py
|       |-- user.py
|       |-- blog.py
|   |-- dependencies/
|       |-- __init__.py
|       |-- authentication.py
|   |-- routers/
|       |-- __init__.py
|       |-- auth.py
|       |-- blogs.py
|       |-- dashboard.py
|-- Dockerfile
|-- requirements.txt
|-- .env
|-- README.md


## Code Files
app/__init__.py: Empty file indicating that app is a Python package.

app/main.py: Main file containing the FastAPI application instance (app), route configurations, and the entry point to run the application.

app/models/__init__.py: Empty file indicating that models is a Python package.

app/models/user.py: Defines the Pydantic model for user data (User, UserCreate, UserUpdate).

app/models/blog.py: Defines the Pydantic model for blog data (Blog, BlogCreate, BlogUpdate).

app/dependencies/__init__.py: Empty file indicating that dependencies is a Python package.

app/dependencies/authentication.py: Contains code related to user authentication, including token creation and verification.

app/routers/__init__.py: Empty file indicating that routers is a Python package.

app/routers/auth.py: Implements authentication-related API endpoints such as user registration, login, profile update, and tag management.

app/routers/blogs.py: Implements CRUD operations for blogs, including creating, retrieving, updating, and deleting blogs.

app/routers/dashboard.py: Implements the dashboard-related endpoint to fetch blogs based on user-followed tags with sorting and pagination.

Dockerfile: Contains instructions for building a Docker image for the FastAPI application. Configures dependencies, exposes ports, and sets the MongoDB URI.

requirements.txt: Lists the Python dependencies required for the project.

.env: Configuration file for environment variables, including the MongoDB URI.

README.md: Project documentation providing an overview, setup instructions, and other relevant information.

This project structure follows a modular approach with separate files for models, dependencies, and routers. The code is organized to promote maintainability and readability. The FastAPI application is defined in the main.py file, and various functionalities are encapsulated in separate modules. The Dockerfile allows for containerization and easy deployment of the application. The README provides instructions for setting up the project and includes details about the technology stack, endpoints, and deployment.

## Contributing
Feel free to contribute to the project. Create a fork of the repository, make your changes, and submit a pull request.
