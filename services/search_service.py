from typing import List
from models.video import Video
from datetime import datetime

# Mock dataset
MOCK_VIDEOS = [
    Video(
        video_id=1,
        title="Intro to Cloud Computing",
        course_id="CS5356",
        course_name="Cloud Computing",
        prof_name="Prof. Ferguson",
        uploaded_at=datetime(2025, 9, 20, 10, 0),
        gcs_path="gs://videos/cs5356/lecture1.mp4"
    ),
    Video(
        video_id=2,
        title="Kubernetes Basics",
        course_id="CS5356",
        course_name="Cloud Computing",
        prof_name="Prof. Ferguson",
        uploaded_at=datetime(2025, 9, 22, 10, 0),
        gcs_path="gs://videos/cs5356/lecture2.mp4"
    )
]

def search_videos(q: str = None, course_id: str = None, prof: str = None, limit: int = 20) -> List[Video]:
    results = [
        v for v in MOCK_VIDEOS
        if (not q or q.lower() in v.title.lower())
        and (not course_id or v.course_id == course_id)
        and (not prof or prof.lower() in v.prof_name.lower())
    ]
    return results[:limit]
