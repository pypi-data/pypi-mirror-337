import abc
import typing as t

from kit_up.core import models
from kit_up.core.clauses import base as bfs
from kit_up.core.data_mappers import base as base_mappers
from kit_up.core.mixins import crud
from kit_up.core.repositories import base
from kit_up.core.repositories import exceptions as repo_excs

# Sync


class AbstractSemiCrudRepository(
    base.AbstractRepository,
    crud.AbstractSemiCrud,
    abc.ABC,
):
    pass
    # TODO(d.burmistrov): functools.singledispatchmethod
    # @abc.abstractmethod
    # def destroy(self, identity_or_model) -> None:
    #     raise NotImplementedError


class RequiresCrudRepositoryMixin(base.RequiresRepositoryMixin):
    _repository: AbstractSemiCrudRepository


# TODO(d.burmistrov):
#   https://docs.python.org/3/library/functools.html#functools.singledispatchmethod
class AbstractDataMappedSemiCrudRepository(
    AbstractSemiCrudRepository,
    base_mappers.RequiresDataMapperMixin,
    abc.ABC,
):
    def get_model_type(self) -> type[models.BaseModel]:
        return self._data_mapper.model_type

    @abc.abstractmethod
    def _create(self, inputs) -> t.Any:
        raise NotImplementedError

    # TODO(d.burmistrov): support sql/repo features
    # from kit_up.flavors.sql import base
    # def create(self, input, *inputs, _flavors: t.Iterable[base.SqlFlavor]
    #      ) -> tuple:
    def create(self, input, *inputs) -> tuple:
        initialized = tuple(
            self._data_mapper.initialize(item) for item in (input, *inputs)
        )
        result = self._create(initialized)
        models = tuple(self._data_mapper.to_model(item) for item in result)
        return models

    def pick(self, identity, *clauses: bfs.BaseClause):
        filter = self._data_mapper.model_to_filter(identity)
        with repo_excs.EntityNotFoundExc.reraise():
            return self.get(filter)

    @abc.abstractmethod
    def _filter(self, *clauses: bfs.BaseClause):
        raise NotImplementedError

    def filter(self, *clauses: bfs.BaseClause) -> t.Iterable:
        data = self._filter(*clauses)
        result = tuple(self._data_mapper.to_model(item) for item in data)
        return result

    @abc.abstractmethod
    def update(self, model, *models) -> None:
        raise NotImplementedError

    def destroy(self, identity_or_model) -> None:
        filter = self._data_mapper.model_to_filter(identity_or_model)
        return super().erase(filter)


# Async


class AbstractAsyncSemiCrudRepository(
    base.AbstractAsyncRepository,
    crud.AbstractAsyncSemiCrud,
    abc.ABC,
):
    pass


class RequiresAsyncCrudRepositoryMixin(base.RequiresRepositoryMixin):
    _repository: AbstractAsyncSemiCrudRepository


class AbstractDataMappedAsyncSemiCrudRepository(
    AbstractAsyncSemiCrudRepository,
    base_mappers.RequiresDataMapperMixin,
    abc.ABC,
):
    def get_model_type(self) -> type[models.BaseModel]:
        return self._data_mapper.model_type

    @abc.abstractmethod
    async def _create(self, inputs) -> t.Any:
        raise NotImplementedError

    # TODO(d.burmistrov): support sql/repo features
    # from kit_up.flavors.sql import base
    # def create(self, input, *inputs, _flavors: t.Iterable[base.SqlFlavor]
    #      ) -> tuple:
    async def create(self, input, *inputs) -> tuple:
        initialized = tuple(
            self._data_mapper.initialize(item) for item in (input, *inputs)
        )
        result = await self._create(initialized)
        models = tuple(self._data_mapper.to_model(item) for item in result)
        return models

    async def pick(self, identity, *clauses: bfs.BaseClause):
        filter = self._data_mapper.model_to_filter(identity)
        with repo_excs.EntityNotFoundExc.reraise():
            return await self.get(filter)

    @abc.abstractmethod
    async def _filter(self, *clauses: bfs.BaseClause):
        raise NotImplementedError

    async def filter(self, *clauses: bfs.BaseClause) -> t.Iterable:
        data = await self._filter(*clauses)
        result = tuple(self._data_mapper.to_model(item) for item in data)
        return result

    @abc.abstractmethod
    async def update(self, model, *models) -> None:
        raise NotImplementedError

    async def destroy(self, identity_or_model) -> int | None:
        filter = self._data_mapper.model_to_filter(identity_or_model)
        return await super().erase(filter)
