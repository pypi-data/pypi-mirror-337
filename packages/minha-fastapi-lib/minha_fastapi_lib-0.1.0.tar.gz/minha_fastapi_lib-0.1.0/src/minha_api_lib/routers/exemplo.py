from fastapi import APIRouter

router = APIRouter(prefix="/exemplo", tags=["exemplo"])

@router.get("/")
def read_exemplo():
    return {"message": "Olá do módulo exemplo!"}