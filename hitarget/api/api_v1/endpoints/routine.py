from starlette.status import HTTP_200_OK
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from hitarget.core.mongodb import AsyncIOMotorDatabase, get_database
from hitarget.models.routine import FormAddRoutine, RoutineInResponse
from hitarget.business import routine as routine_bus

router = APIRouter(prefix="/routine", tags=["Routine"])


@router.post("", response_description="Write down a new daily routine")
async def add_routine(form: FormAddRoutine, db: AsyncIOMotorDatabase = Depends(get_database)):
    created_routine = await routine_bus.create_routine(db, form)
    response = RoutineInResponse(**created_routine.dict())
    return JSONResponse(status_code=HTTP_200_OK,
                        content=jsonable_encoder(response))
