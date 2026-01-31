import sys
import os

# Add local libs to path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LIBS_DIR = os.path.join(os.path.dirname(BASE_DIR), "pylibs")
if os.path.exists(LIBS_DIR):
    sys.path.insert(0, LIBS_DIR)

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

from backend.models import KeyResponse, ErrorResponse
from backend.generator import generate_key_logic
from backend.database import init_db, get_key

app = FastAPI(title="Automatic Key Generator")

# CORS to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Database on startup
@app.on_event("startup")
def startup_event():
    init_db()

# Mount storage for static serving of STLs
# Using absolute path for safety
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_DIR = os.path.join(BASE_DIR, "storage")
app.mount("/storage", StaticFiles(directory=STORAGE_DIR), name="storage")

@app.post("/generate", response_model=KeyResponse)
def generate_endpoint():
    try:
        result = generate_key_logic()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{key_id}")
def download_key(key_id: int):
    key = get_key(key_id)
    if not key:
        raise HTTPException(status_code=404, detail="Key not found")
    
    # Construct full path
    # key['stl_path'] is relative: "storage/keys/key_....stl"
    # We need absolute path for FileResponse
    file_path = os.path.join(BASE_DIR, key['stl_path'])
    
    filename = os.path.basename(file_path)
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/octet-stream'
    )

# Optional: Serve frontend if we want a unified server, 
# but the plan implies frontend might be separate. 
# However, for ease of use, let's mount the frontend static files too?
# "Frontend: ... static frontend hosting".
# I'll rely on opening index.html directly or serving via python http.server for frontend.
# But mounting it here makes it a complete app.
# Let's mount frontend at root.
from fastapi.responses import HTMLResponse

# Mount frontend at root
FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), "frontend")
if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

