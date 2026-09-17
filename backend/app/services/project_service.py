from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.schemas.project import ProjectCreate


async def create_project(
    db: AsyncSession,
    data: ProjectCreate,
) -> Project:
    project = Project(
        organization_id=data.organization_id,
        name=data.name,
        slug=data.slug,
        description=data.description,
    )

    db.add(project)
    await db.commit()
    await db.refresh(project)

    return project