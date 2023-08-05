from endpoints import accounts_api
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(accounts_api.router, prefix="/accounts", tags=["accounts"])
