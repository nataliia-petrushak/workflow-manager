from fastapi import FastAPI

from src.routers import router as workflow_router

app = FastAPI()
app.include_router(workflow_router.routes)

