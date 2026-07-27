from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

from app.db.session import get_db
from app.models.semester import Semester
from app.schemas.semester import SemesterResponse, SemesterCreate

router = APIRouter()

@router.get("/", response_model=List[SemesterResponse])
async def get_semesters(major_id: Optional[int] = Query(None), db: AsyncSession = Depends(get_db)):
    stmt = select(Semester)
    if major_id is not None:
        stmt = stmt.where(Semester.major_id == major_id)
    stmt = stmt.order_by(Semester.id.asc())
    result = await db.execute(stmt)
    return result.scalars().all()

@router.get("/{semester_id}", response_model=SemesterResponse)
async def get_semester(semester_id: int, db: AsyncSession = Depends(get_db)):
    semester = await db.get(Semester, semester_id)
    if not semester:
        raise HTTPException(status_code=404, detail="Semester not found")
    return semester

@router.post("/", response_model=SemesterResponse)
async def create_semester(semester_in: SemesterCreate, db: AsyncSession = Depends(get_db)):
    new_semester = Semester(**semester_in.model_dump())
    db.add(new_semester)
    await db.commit()
    await db.refresh(new_semester)
    return new_semester

@router.put("/{semester_id}", response_model=SemesterResponse)
async def update_semester(semester_id: int, semester_in: SemesterCreate, db: AsyncSession = Depends(get_db)):
    semester = await db.get(Semester, semester_id)
    if not semester:
        raise HTTPException(status_code=404, detail="Semester not found")
    for key, value in semester_in.model_dump(exclude_unset=True).items():
        setattr(semester, key, value)
    await db.commit()
    await db.refresh(semester)
    return semester

@router.delete("/{semester_id}")
async def delete_semester(semester_id: int, db: AsyncSession = Depends(get_db)):
    semester = await db.get(Semester, semester_id)
    if not semester:
        raise HTTPException(status_code=404, detail="Semester not found")
    await db.delete(semester)
    await db.commit()
    return {"status": "success"}
