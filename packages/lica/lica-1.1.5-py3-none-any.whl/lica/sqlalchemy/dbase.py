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

from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

url = decouple.config("DATABASE_URL")

# 'check_same_thread' is only needed in SQLite ....
engine = create_engine(url, connect_args={"check_same_thread": False})

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


class Model(DeclarativeBase):
    metadata = metadata


Session = sessionmaker(engine, expire_on_commit=True)

__all__ = ["url", "engine", "metadata", "Model", "Session"]
