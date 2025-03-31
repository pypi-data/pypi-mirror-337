# ----------------------------------------------------------------------
# Copyright (c) 2024 Rafael Gonzalez.
#
# See the LICENSE file for details
# ----------------------------------------------------------------------

# --------------------
# System wide imports
# -------------------

# ---------------------
# Third party libraries
# ---------------------

import decouple

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs

url = decouple.config("DATABASE_URL")

# 'check_same_thread' is only needed in SQLite ....
engine = create_async_engine(url, connect_args={"check_same_thread": False})

metadata = MetaData(
    # For the different artifacts (indexes, constraints, etc.)
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)


class Model(AsyncAttrs, DeclarativeBase):
    metadata = metadata


AsyncSession = async_sessionmaker(engine, expire_on_commit=False)

__all__ = ["url", "engine", "metadata", "Model", "AsyncSession"]
