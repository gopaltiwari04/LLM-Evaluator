from sqlalchemy.ext.asyncio import AsyncSession

from app.models.organization import Organization
from app.schemas.organization import OrganizationCreate


async def create_organization(
    db: AsyncSession,
    data: OrganizationCreate,
) -> Organization:
    organization = Organization(
        name=data.name,
        slug=data.slug,
    )

    db.add(organization)
    await db.commit()
    await db.refresh(organization)

    return organization