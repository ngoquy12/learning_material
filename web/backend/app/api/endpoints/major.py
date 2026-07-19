from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.db.session import get_db
from app.models.major import Major
from app.schemas.major import MajorResponse, MajorCreate

router = APIRouter()

@router.get("/", response_model=List[MajorResponse])
async def get_majors(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Major))
    return result.scalars().all()

@router.post("/", response_model=MajorResponse)
async def create_major(major_in: MajorCreate, db: AsyncSession = Depends(get_db)):
    new_major = Major(**major_in.model_dump())
    db.add(new_major)
    await db.commit()
    await db.refresh(new_major)
    return new_major
