import sys
import os

# Inject path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LIBS_DIR = os.path.join(BASE_DIR, "pylibs")
if os.path.exists(LIBS_DIR):
    sys.path.insert(0, LIBS_DIR)

# Add project root to path (so 'backend' is recognized as a package)
sys.path.append(BASE_DIR)

try:
    print("Importing modules...")
    from backend.generator import generate_key_logic
    from backend.database import init_db
    print("Modules imported successfully.")

    print("Initializing DB...")
    init_db()

    print("Generating key...")
    result = generate_key_logic()
    print(f"Success! Key Generated: {result}")
    
    print("Verification passed.")
except Exception as e:
    print(f"Verification FAILED: {e}")
    import traceback
    traceback.print_exc()
