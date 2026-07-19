from fastapi import APIRouter
from app.api.endpoints import program, major, semester, course, session, lesson, artifact, pipeline

api_router = APIRouter()

api_router.include_router(program.router, prefix="/programs", tags=["programs"])
api_router.include_router(major.router, prefix="/majors", tags=["majors"])
api_router.include_router(semester.router, prefix="/semesters", tags=["semesters"])
api_router.include_router(course.router, prefix="/courses", tags=["courses"])
api_router.include_router(session.router, prefix="/sessions", tags=["sessions"])
api_router.include_router(lesson.router, prefix="/lessons", tags=["lessons"])
api_router.include_router(artifact.router, prefix="/artifacts", tags=["artifacts"])
api_router.include_router(pipeline.router, prefix="/pipeline", tags=["pipeline"])
