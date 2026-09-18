from fastapi import APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.db.database import get_db
from app.schemas.api_key import APIKeyCreate, APIKeyResponse
from app.services.api_key_service import create_api_key


router = APIRouter(
    prefix="/api-keys",
    tags=["api-keys"],
)


@router.post(
    "",
    response_model=APIKeyResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_api_key_endpoint(
    data: APIKeyCreate,
    db: AsyncSession = Depends(get_db),
) -> APIKeyResponse:
    try:
        api_key, raw_key = await create_api_key(
            db=db,
            data=data,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    return APIKeyResponse(
        id=api_key.id,
        project_id=api_key.project_id,
        name=api_key.name,
        api_key=raw_key,
    )