import random
import hashlib
from backend.database import save_key, hash_exists
from backend.geometry import build_stl

# Constants matching specs
MIN_DEPTH = 0.5
MAX_DEPTH = 2.5
MAX_ADJ_DIFF = 1.5
NUM_CUTS = 6

def generate_cut_depths() -> list[float]:
    """Generates a list of random cut depths."""
    return [round(random.uniform(MIN_DEPTH, MAX_DEPTH), 2) for _ in range(NUM_CUTS)]

def is_valid(cuts: list[float]) -> bool:
    """
    Validates the cut depths against constraints:
    1. Each depth between 0.5 and 2.5 (Implicit by generation, but good to check).
    2. Adjacent cut difference <= 1.5mm.
    """
    for d in cuts:
        if not (MIN_DEPTH <= d <= MAX_DEPTH):
            return False
            
    for i in range(len(cuts) - 1):
        diff = abs(cuts[i] - cuts[i+1])
        if diff > MAX_ADJ_DIFF:
            return False
    return True

def generate_hash(cuts: list[float]) -> str:
    """
    Generates SHA256 hash from cuts array + 'flat-single-sided'.
    """
    # 1. Convert array to string
    cuts_str = str(cuts)
    # 2. Append identifier
    payload = cuts_str + "flat-single-sided"
    # 3. Hash
    return hashlib.sha256(payload.encode()).hexdigest()

def generate_key_logic():
    """
    Orchestrates the generation of a unique valid key.
    Returns dictionary with key_id and stl_url.
    """
    attempts = 0
    while True:
        attempts += 1
        # Safety break to prevent infinite loops if constraints are too tight (unlikely here)
        if attempts > 10000:
            raise Exception("Failed to generate unique key after many attempts")

        cuts = generate_cut_depths()
        
        if not is_valid(cuts):
            continue
            
        h = generate_hash(cuts)
        
        if hash_exists(h):
            continue
            
        # Unique and Valid
        try:
            # Build STL
            rel_path = build_stl(cuts, h)
            
            # Save to DB
            save_key(cuts, h, rel_path)
            
            # Retrieve ID (we need to query it back or change save_key to return it)
            # Let's import get_db_connection to get the ID efficiently or change save_key logic.
            # For now, let's just query by hash since it is unique.
            # Importing here to avoid circular imports? No, database is separate.
            from backend.database import get_db_connection
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("SELECT id FROM keys WHERE hash = ?", (h,))
            row = c.fetchone()
            conn.close()
            
            if row:
                return {"key_id": row['id'], "stl_url": rel_path}
            else:
                raise Exception("Failed to retrieve saved key")
                
        except Exception as e:
            # Handle geometry errors or DB errors
            print(f"Error generating key: {e}")
            raise e
