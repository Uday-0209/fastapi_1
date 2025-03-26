from fastapi import APIRouter

router = APIRouter()


@router.get('/auth/')
async def auth_get():
    return{'User':'Auntheticated'}
