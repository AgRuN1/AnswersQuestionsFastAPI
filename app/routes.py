from fastapi import APIRouter

from app.controllers import questions_controller, answers_controller


def get_apps_router():
    router = APIRouter()
    router.include_router(questions_controller.router)
    router.include_router(answers_controller.router)
    return router