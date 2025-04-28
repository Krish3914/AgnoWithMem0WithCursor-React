from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import os
import shutil
from pathlib import Path
from typing import List
import json
from PIL import Image
import io
import base64
from react_generator import ReactGenerator
from groq import AsyncGroq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# os.environ["GROQ_API_KEY"] = "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"
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ReactGenerator
react_generator = ReactGenerator()

# Create directories for uploads and generated projects
UPLOAD_DIR = Path("uploads")
GENERATED_DIR = Path("generated_projects")
UPLOAD_DIR.mkdir(exist_ok=True)
GENERATED_DIR.mkdir(exist_ok=True)

async def get_image_description(image_path: Path) -> str:
    """Get a description of the image using Groq API"""
    try:
        # Read and encode image
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Get API key
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
        
        # Create Groq client
        client = AsyncGroq(api_key=api_key)
        
        # Get image description
        response = await client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert at analyzing images. Provide a detailed description of the image, focusing on any text, UI elements, or design requirements that would be relevant for creating a React application."
                },
                {
                    "role": "user",
                    "content": f"Please analyze this image and provide a detailed description focusing on UI elements and requirements: {encoded_string[:10000]}"  # Limit the size of the encoded image
                }
            ],
            max_tokens=500  # Limit the response size
        )
        
        return response.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Save uploaded file
        file_path = UPLOAD_DIR / file.filename
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Get image description
        image_description = await get_image_description(file_path)
        
        # Generate React project
        project_name = f"react_project_{file.filename.split('.')[0]}"
        project_path = GENERATED_DIR / project_name
        
        # Generate complete React project
        result = react_generator.generate_react_project(image_description, project_path)
        
        return JSONResponse({
            "message": "React project generated successfully",
            "image_description": image_description,
            "project_name": project_name,
            "project_path": str(project_path),
            "components": result["components"]
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/project/{project_name}")
async def get_project(project_name: str):
    try:
        project_path = GENERATED_DIR / project_name
        if not project_path.exists():
            raise HTTPException(status_code=404, detail="Project not found")
        
        # List all files in the project
        files = []
        for root, _, filenames in os.walk(project_path):
            for filename in filenames:
                file_path = Path(root) / filename
                relative_path = file_path.relative_to(project_path)
                files.append(str(relative_path))
        
        return JSONResponse({
            "project_name": project_name,
            "files": files
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 