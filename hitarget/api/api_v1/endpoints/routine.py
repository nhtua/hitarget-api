from starlette.status import HTTP_200_OK
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from hitarget.core.mongodb import AsyncIOMotorDatabase, get_database
from hitarget.models.user import UserInResponse
from hitarget.models.routine import FormAddRoutine, RoutineInResponse, CheckpointInRequest
from hitarget.business import routine as routine_bus
from hitarget.services.authentication import get_current_authorized_user

router = APIRouter(prefix="/routine", tags=["Routine"])


@router.post("", response_description="Write down a new daily routine")
async def add_routine(
    form: FormAddRoutine,
    db: AsyncIOMotorDatabase = Depends(get_database),
    user: UserInResponse = Depends(get_current_authorized_user)
):
    created_routine = await routine_bus.create_routine(db, form, user.id)
    response = RoutineInResponse(**created_routine.dict())
    return JSONResponse(status_code=HTTP_200_OK,
                        content=jsonable_encoder(response))


@router.get("", response_description="Get list of routines")
async def list_routine(
    db: AsyncIOMotorDatabase = Depends(get_database),
    user: UserInResponse = Depends(get_current_authorized_user)
):
    routines = await routine_bus.get_routine_by_user(db, user_id=user.id)
    return JSONResponse(status_code=HTTP_200_OK,
                        content=jsonable_encoder(routines))


@router.put("/checkpoint", response_description="Update status of today checkpoint")
async def update_checkpoint(
    checkpoint: CheckpointInRequest,
    db: AsyncIOMotorDatabase = Depends(get_database),
    user: UserInResponse = Depends(get_current_authorized_user)
):
    routine = await routine_bus.update_checkpoint(db, checkpoint, user_id=user.id)
    return JSONResponse(status_code=HTTP_200_OK,
                        content=jsonable_encoder(routine))
