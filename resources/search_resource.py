from fastapi import APIRouter, Query, Path
from typing import List
from models.video import Video
from services.search_service import search_videos
from utils.auth import verify_token
from fastapi import Depends

router = APIRouter()

@router.get("/search", response_model=List[Video])
def search(
    q: str = Query(None),
    course_id: str = None,
    prof: str = None,
    limit: int = 20,
    user=Depends(verify_token)  # stub auth
):
    if user.get("role") == "student" and course_id == "FACULTY_ONLY":
        return []
    return search_videos(q, course_id, prof, limit)

# Health check (already implemented)
@router.get("/healthz")
def healthz():
    return {"ok": True}

# POST stub
@router.post("/search")
def create_search():
    return {"detail": "Not implemented"}

# PUT stub
@router.put("/search/{video_id}")
def update_search(video_id: int = Path(..., description="ID of the video to update")):
    return {"detail": f"Not implemented for video_id {video_id}"}

# DELETE stub
@router.delete("/search/{video_id}")
def delete_search(video_id: int = Path(..., description="ID of the video to delete")):
    return {"detail": f"Not implemented for video_id {video_id}"}
