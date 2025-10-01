from pydantic import BaseModel
from datetime import datetime

class Video(BaseModel):
    video_id: int
    title: str
    course_id: str
    course_name: str
    prof_name: str
    uploaded_at: datetime
    gcs_path: str
