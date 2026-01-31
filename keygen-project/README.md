# Automatic Physical Key 3D Generation System

A web-based system for generating unique, manufacturable 3D key models (STL) for key shops.

## Features
- **Automatic Generation**: Creates new key designs with unique cut patterns.
- **Uniqueness Guarantee**: Uses SHA256 hashing to ensure no two keys are identical.
- **3D Preview**: Interactive WebGL preview using Three.js.
- **Parametric Modeling**: Uses CadQuery to generate watertight, CNC-ready STL files.

## Screenshots
![Main Interface](assets/screenshot_main.png)
*Figure 1: Main generation interface with Gold Key preview*

![Generated Key](assets/screenshot_generated.png)
*Figure 2: Successfully generated unique key ID*

## Project Structure
```
keygen-project/
├── backend/            # FastAPI Setup & Logic
│   ├── main.py         # Entry point
│   ├── generator.py    # Key generation logic
│   ├── geometry.py     # CadQuery 3D modeling
│   ├── database.py     # SQLite management
│   └── storage/        # Generated STL files
├── frontend/           # Static Web Assets
│   ├── index.html
│   ├── style.css
│   └── app.js
├── pylibs/             # Local dependencies (if isolated env unavailable)
└── README.md
```

## Setup & Running

### Prerequisites
- Python 3.10+
- Internet access for initial dependency download (or pre-installed libs)

### Installation
The project attempts to use local libraries in `pylibs` to avoid system conflicts.

1. **Install Dependencies** (if not already done):
   ```bash
   pip install --target=./pylibs fastapi uvicorn cadquery pydantic
   ```
   *Note: This might take a few minutes due to CadQuery/OCP binaries.*

2. **Run the Server**:
   ```bash
   python3 backend/main.py
   ```
   The server will start on `http://0.0.0.0:8000`.

3. **Access the Application**:
   Open a web browser and navigate to:
   [http://localhost:8000](http://localhost:8000)

## Usage
1. Click **GENERATE NEW KEY**.
2. Wait for the server to generate a unique design and render the 3D model.
3. Use your mouse to rotate and inspect the key in the preview window.
4. Click **DOWNLOAD STL FILE** to save the file for manufacturing.

## Technical Details
- **Units**: All dimensions are in millimeters.
- **Format**: Binary STL.
- **Database**: `backend/keys.db` (SQLite).
