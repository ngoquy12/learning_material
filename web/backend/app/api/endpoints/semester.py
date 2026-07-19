from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.db.session import get_db
from app.models.semester import Semester
from app.schemas.semester import SemesterResponse, SemesterCreate

router = APIRouter()

@router.get("/", response_model=List[SemesterResponse])
async def get_semesters(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Semester))
    return result.scalars().all()

@router.post("/", response_model=SemesterResponse)
async def create_semester(semester_in: SemesterCreate, db: AsyncSession = Depends(get_db)):
    new_semester = Semester(**semester_in.model_dump())
    db.add(new_semester)
    await db.commit()
    await db.refresh(new_semester)
    return new_semester
