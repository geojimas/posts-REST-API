from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router
from config import Base, engine
import uvicorn

# Database  creation & Migrations
def create_database():
    print("Creating database ....")
    return Base.metadata.create_all(bind=engine)


# Call the function to create the database
create_database()

# init Fastapi
app = FastAPI()

# Cors
origins = ["http://localhost:8000"]

# Apply Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routes
app.include_router(router)


@app.get('/')
async def index():
    return {
        "API is running...": "go to /docs"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)