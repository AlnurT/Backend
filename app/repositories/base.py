from asyncpg import ForeignKeyViolationError
from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import NoResultFound, IntegrityError

from app.exceptions import ObjectNotFoundException, ObjectAlreadyExistsException
from app.repositories.mappers.base import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def get_all(self):
        return await self.get_filtered()

    async def get_filtered(self, *filter, **filter_by):
        query = (
            select(self.model)
            .filter(*filter)
            .filter_by(**filter_by)
        )

        result = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(model) for model in result.scalars().all()
        ]

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        res = result.scalars().one_or_none()
        if res is None:
            return None

        return self.mapper.map_to_domain_entity(res)

    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            res = result.scalar_one()
        except NoResultFound:
            raise ObjectNotFoundException

        return self.mapper.map_to_domain_entity(res)

    async def add(self, data: BaseModel):
        add_stmt = (
            insert(self.model)
            .values(**data.model_dump())
            .returning(self.model)
        )
        try:
            result = await self.session.execute(add_stmt)
        except IntegrityError:
            raise ObjectNotFoundException

        res = result.scalars().one()
        return self.mapper.map_to_domain_entity(res)

    async def add_bulk(self, data: list[BaseModel]):
        add_stmt = (
            insert(self.model)
            .values([item.model_dump() for item in data])
        )
        await self.session.execute(add_stmt)

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        edit_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        try:
            await self.session.execute(edit_stmt)
        except IntegrityError:
            raise ObjectNotFoundException

    async def delete(self, **filter_by):
        delete_stmt = (
            delete(self.model)
            .filter_by(**filter_by)
        )
        try:
            await self.session.execute(delete_stmt)
        except IntegrityError:
            raise ObjectNotFoundException
