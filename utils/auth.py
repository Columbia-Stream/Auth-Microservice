from fastapi import Header, HTTPException

def verify_token(authorization: str = Header(None)):
    """
    Stubbed authentication.
    Later: verify with authentication microservice.
    For now: just return a fake user if header exists.
    """
    if not authorization:
        # Allow unauthenticated for testing
        return {"sub": "guest", "role": "student", "email": "guest@columbia.edu"}

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth header")

    # Return a fake payload for now
    return {
        "sub": "demo123",
        "role": "faculty",
        "email": "demo123@columbia.edu"
    }
