import httpx

import datetime

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from starlette import status

from models import get_session, DBTemperature, DBCity, get_async_session

from temperature_api.schemas import (
    TemperatureRead,
    TemperatureUpdate
)

from .additional_funcs_for_api import get_geocoded_city, get_temperatures


SessionDep = Annotated[Session, Depends(get_session)]

AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]

router = APIRouter()


@router.post("/temperatures/update")
async def update_temperatures(session: AsyncSessionDep):
    result = await session.scalars(select(DBCity))
    cities = result.all()

    async with httpx.AsyncClient(timeout=10) as client:
        for city in cities:
            try:
                coordinates = await get_geocoded_city(city.name, client)
                temp = await get_temperatures(coordinates, client)

                obj = DBTemperature(
                    city_id=city.id,
                    date_time=datetime.datetime.now(datetime.UTC),
                    temperature=temp,
                )
                session.add(obj)

            except Exception as e:
                # logs
                print(f"Failed for city {city.name}: {e}")

    await session.commit()

    return {"success": True}


@router.get("/temperatures")
def list_temperatures(session: SessionDep):
    stmt = select(DBTemperature)
    return session.scalars(stmt).all()


@router.get("/temperatures/{city_id}", response_model=TemperatureRead)
def get_temperature(city_id: int, session: SessionDep):
    temp_obj = session.get(DBTemperature, city_id)

    if temp_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )

    return temp_obj
