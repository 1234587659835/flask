from fastapi import APIRouter
from .accpwdService import storeAdd  # 修改匯入路徑

router = APIRouter()

@router.get("'/api/accpwd/get'")
async def hellow():
    result = storeAdd(5, 2)
    return {"message": result}
