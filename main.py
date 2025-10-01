#source venv/bin/activate
from fastapi import FastAPI
from resources import search_resource

app = FastAPI(title="Search Service")
app.include_router(search_resource.router)
