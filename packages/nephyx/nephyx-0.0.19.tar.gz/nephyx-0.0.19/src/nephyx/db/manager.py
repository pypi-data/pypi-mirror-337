import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Callable, Dict, Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

logger = logging.getLogger(__name__)


class DatabaseManager:

    def __init__(self, connection_options: Dict[str, Any]):
        self.connection_options = connection_options
        self.engine: Optional[AsyncEngine] = None
        self.async_session_factory: Optional[async_sessionmaker[AsyncSession]] = None

    def init_engine(self) -> AsyncEngine:
        if self.engine is None:
            logger.info("Initializing database engine")
            self.engine = create_async_engine(
                self.connection_options.pop("url"),
                **self.connection_options
            )
            self.async_session_factory = async_sessionmaker(
                self.engine,
                expire_on_commit=False,
                autoflush=False,
            )

        return self.engine

    def get_session_factory(self) -> async_sessionmaker[AsyncSession]:
        if self.async_session_factory is None:
            self.init_engine()

        return self.async_session_factory

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        session_factory = self.get_session_factory()

        async with session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e

    async def close(self) -> None:
        if self.engine:
            logger.info("Closing database engine")
            await self.engine.dispose()
            self.engine = None
            self.async_session_factory = None


# Global database manager instance
db_manager: Optional[DatabaseManager] = None


def init_db(connection_options: Dict[str, Any]) -> DatabaseManager:
    global db_manager

    if db_manager is None:
        db_manager = DatabaseManager(connection_options)
        db_manager.init_engine()

    return db_manager


async def close_db() -> None:
    global db_manager

    if db_manager:
        await db_manager.close()
        db_manager = None


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    if db_manager is None:
        raise RuntimeError("Database not initialized. Call init_db first.")

    async with db_manager.session() as session:
        yield session


# Dependency for injecting DB session
DbSession = Callable[[], AsyncGenerator[AsyncSession, None]]
db_session_dependency = Depends(get_db_session)
