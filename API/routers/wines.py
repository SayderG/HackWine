from typing import List
from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import StreamingResponse

from database.base import AsyncDatabase
from database.repositories.WineRepository import WineRepository
from database.models.Wine import WineCreate, WineRead, WineUpdate
from fastapi_cache.decorator import cache
import qrcode
from PIL import Image
import io
from API.redis import get_redis

router = APIRouter()


@router.post('/', name='create wine track')
async def create_wine(wine: WineCreate, session=Depends(AsyncDatabase.get_session)):
    return await WineRepository(session).create(wine.__dict__)


@router.get('/all', name='get all wines', response_model=List[WineRead])
@cache(expire=60)
async def all_wines(session=Depends(AsyncDatabase.get_session)):
    return await WineRepository(session).all()


@router.get('/{wine_id}', name='get wine by id', response_model=WineRead)
@cache(expire=120)
async def wine_by_id(wine_id: int, session=Depends(AsyncDatabase.get_session)):
    return await WineRepository(session).by_id(wine_id)


@router.get('/generate_qr/{wine_id}', name='generate QR code for wine')
async def generate_qr(wine_id: int, session=Depends(AsyncDatabase.get_session)):
    wine = await WineRepository(session).by_id(wine_id)
    if wine is None:
        raise HTTPException(status_code=404, detail='Wine not found')

    qr_data = f'Product: {wine.name}\nLocation: {wine.location}\nStatus: {wine.status}'
    qr_code = qrcode.make(qr_data)

    image_stream = io.BytesIO()
    qr_code.save(image_stream, format='PNG')
    image_stream.seek(0)
    redis = await get_redis()
    await redis.set(wine_id, image_stream.getvalue())

    return {'message': 'QR code generated and saved in Redis'}


@router.get('/get_qr/{wine_id}', name='get QR code for wine')
async def get_qr(wine_id: int):
    redis = await get_redis()
    qr_image = await redis.get(wine_id)
    if qr_image is None:
        raise HTTPException(status_code=404, detail='QR code not found')

    image = Image.open(io.BytesIO(qr_image))
    image_stream = io.BytesIO()
    image.save(image_stream, format='PNG')
    image_stream.seek(0)

    return StreamingResponse(content=image_stream, media_type='image/png')


@router.put('/update/{wine_id}', name='update wine information by id')
async def update_wine(wine_id: int, wine_update: WineUpdate, session=Depends(AsyncDatabase.get_session)):
    wine_repo = WineRepository(session)
    wine = await wine_repo.by_id(wine_id)
    if wine is None:
        raise HTTPException(status_code=404, detail='Wine not found')

    await wine_repo.update(wine, wine_update)
    return {'message': 'Wine information updated successfully'}


@router.delete('/{wine_id}', name='delete wine by id')
async def del_wine(wine_id: int, session=Depends(AsyncDatabase.get_session)):
    return await WineRepository(session).delete(wine_id)
