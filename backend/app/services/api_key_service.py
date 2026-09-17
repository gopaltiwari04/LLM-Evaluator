from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import generate_api_key
from app.models.api_key import APIKey
from app.models.project import Project
from app.schemas.api_key import APIKeyCreate


async def create_api_key(
    db: AsyncSession,
    data: APIKeyCreate,
) -> tuple[APIKey, str]:
    # Verify that the project exists.
    result = await db.execute(
        select(Project).where(Project.id == data.project_id)
    )
    project = result.scalar_one_or_none()

    if project is None:
        raise ValueError("Project not found")

    raw_key, key_hash = generate_api_key()

    api_key = APIKey(
        project_id=data.project_id,
        name=data.name,
        key_hash=key_hash,
    )

    db.add(api_key)

    await db.commit()
    await db.refresh(api_key)

    return api_key, raw_key