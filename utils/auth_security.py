import bcrypt
from typing import Union

# --- Configuration ---
# Bcrypt requires a salt to be mixed with the password for security.
# bcrypt.gensalt() generates a secure, randomized salt.
# The number '12' sets the complexity (work factor); 12 is a secure standard.
SALT_ROUNDS = 12 

def hash_password(password: str) -> str:
    """
    Hashes a plaintext password using bcrypt and returns the hashed string.
    """
    # Convert password string to bytes (required by bcrypt)
    password_bytes = password.encode('utf-8')
    
    # Generate a salt and hash the password
    hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt(SALT_ROUNDS))
    
    # Decode back to a string for storage in the database
    return hashed_bytes.decode('utf-8')

def verify_password(plaintext_password: str, hashed_password: Union[str, bytes]) -> bool:
    """
    Verifies a plaintext password against a stored hash.
    Returns True if they match, False otherwise.
    """
    if isinstance(hashed_password, str):
        # Convert stored hash string back to bytes
        hashed_bytes = hashed_password.encode('utf-8')
    else:
        # Assume it's already bytes
        hashed_bytes = hashed_password
        
    # Verify the password
    # NOTE: bcrypt handles the extraction of the salt from the hash itself.
    return bcrypt.checkpw(plaintext_password.encode('utf-8'), hashed_bytes)