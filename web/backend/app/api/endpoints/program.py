from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.db.session import get_db
from app.models.program import Program
from app.schemas.program import ProgramResponse, ProgramCreate

router = APIRouter()

@router.get("/", response_model=List[ProgramResponse])
async def get_programs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Program))
    return result.scalars().all()

@router.post("/", response_model=ProgramResponse)
async def create_program(program_in: ProgramCreate, db: AsyncSession = Depends(get_db)):
    new_program = Program(**program_in.model_dump())
    db.add(new_program)
    await db.commit()
    await db.refresh(new_program)
    return new_program
