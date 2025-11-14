from sqlalchemy import Column, Integer, MetaData
from sqlalchemy.orm import DeclarativeBase

metadata_ = MetaData()


class MinimalBase(DeclarativeBase):
    __abstract__ = True
    metadata = metadata_


class BaseModel(MinimalBase):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)