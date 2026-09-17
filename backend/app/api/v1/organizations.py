from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.organization import (
    OrganizationCreate,
    OrganizationResponse,
)
from app.services.organization_service import create_organization


router = APIRouter(
    prefix="/organizations",
    tags=["organizations"],
)


@router.post(
    "",
    response_model=OrganizationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_organization_endpoint(
    data: OrganizationCreate,
    db: AsyncSession = Depends(get_db),
) -> OrganizationResponse:
    organization = await create_organization(
        db=db,
        data=data,
    )

    return OrganizationResponse(
        id=organization.id,
        name=organization.name,
        slug=organization.slug,
    )