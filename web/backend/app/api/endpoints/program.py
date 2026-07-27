from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.db.session import get_db
from app.models.program import Program
from app.schemas.program import ProgramResponse, ProgramCreate

router = APIRouter()

@router.get("/", response_model=List[ProgramResponse])
async def get_programs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Program).order_by(Program.id.asc()))
    return result.scalars().all()

@router.get("/{program_id}", response_model=ProgramResponse)
async def get_program(program_id: int, db: AsyncSession = Depends(get_db)):
    program = await db.get(Program, program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    return program

@router.post("/", response_model=ProgramResponse)
async def create_program(program_in: ProgramCreate, db: AsyncSession = Depends(get_db)):
    new_program = Program(**program_in.model_dump())
    db.add(new_program)
    await db.commit()
    await db.refresh(new_program)
    return new_program

@router.put("/{program_id}", response_model=ProgramResponse)
async def update_program(program_id: int, program_in: ProgramCreate, db: AsyncSession = Depends(get_db)):
    program = await db.get(Program, program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    for key, value in program_in.model_dump(exclude_unset=True).items():
        setattr(program, key, value)
    await db.commit()
    await db.refresh(program)
    return program

@router.delete("/{program_id}")
async def delete_program(program_id: int, db: AsyncSession = Depends(get_db)):
    program = await db.get(Program, program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    await db.delete(program)
    await db.commit()
    return {"status": "success"}
