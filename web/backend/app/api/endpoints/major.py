from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

from app.db.session import get_db
from app.models.major import Major
from app.schemas.major import MajorResponse, MajorCreate

router = APIRouter()

@router.get("/", response_model=List[MajorResponse])
async def get_majors(program_id: Optional[int] = Query(None), db: AsyncSession = Depends(get_db)):
    stmt = select(Major)
    if program_id is not None:
        stmt = stmt.where(Major.program_id == program_id)
    stmt = stmt.order_by(Major.id.asc())
    result = await db.execute(stmt)
    return result.scalars().all()

@router.get("/{major_id}", response_model=MajorResponse)
async def get_major(major_id: int, db: AsyncSession = Depends(get_db)):
    major = await db.get(Major, major_id)
    if not major:
        raise HTTPException(status_code=404, detail="Major not found")
    return major

@router.post("/", response_model=MajorResponse)
async def create_major(major_in: MajorCreate, db: AsyncSession = Depends(get_db)):
    new_major = Major(**major_in.model_dump())
    db.add(new_major)
    await db.commit()
    await db.refresh(new_major)
    return new_major

@router.put("/{major_id}", response_model=MajorResponse)
async def update_major(major_id: int, major_in: MajorCreate, db: AsyncSession = Depends(get_db)):
    major = await db.get(Major, major_id)
    if not major:
        raise HTTPException(status_code=404, detail="Major not found")
    for key, value in major_in.model_dump(exclude_unset=True).items():
        setattr(major, key, value)
    await db.commit()
    await db.refresh(major)
    return major

@router.delete("/{major_id}")
async def delete_major(major_id: int, db: AsyncSession = Depends(get_db)):
    major = await db.get(Major, major_id)
    if not major:
        raise HTTPException(status_code=404, detail="Major not found")
    await db.delete(major)
    await db.commit()
    return {"status": "success"}
