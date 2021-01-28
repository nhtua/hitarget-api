from typing import Callable
from fastapi import FastAPI
from loguru import logger

from hitarget.core import mongodb


def create_start_app_handler(app: FastAPI) -> Callable:  # type: ignore
    async def start_app():
        app.state.dbe = await mongodb.connect()

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:  # type: ignore
    @logger.catch
    async def stop_app() -> None:
        await mongodb.disconnect()

    return stop_app
