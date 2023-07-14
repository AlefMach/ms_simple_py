from typing import Callable, Type

from fastapi import Depends
from sqlalchemy.orm import Session

from src.infra.adapters.database.orm.settings import get_session
from src.infra.adapters.repositories.abstract_repository import AbstractRepository


async def get_session_repo():
    async with get_session() as session:
        yield session


def get_repository(repo_type: Type[AbstractRepository]) -> Callable[[Session], AbstractRepository]:
    """Get repository"""

    def __get_repo(session_db: Session = Depends(get_session_repo)) -> AbstractRepository:  # noqa B008
        return repo_type(session=session_db)

    return __get_repo
