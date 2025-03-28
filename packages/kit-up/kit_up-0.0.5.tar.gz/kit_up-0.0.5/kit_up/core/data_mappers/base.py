import typing as t

from kit_up.core.clauses import predicates as dfs
from kit_up.core.mixins import require


def _unwrap_attr(attr, obj):
    if isinstance(attr, str):
        attr = getattr(obj, attr)
    return attr


# class Mappable(t.Protocol):
#     def get_identity_qualifier(self):
#         pass
#
#     def get_identity(self, item):
#         pass
#
#     def as_dict(self, item) -> dict:
#         pass


class AdapterForData:
    def __init__(
        self,
        target_type: type,
        get_identity_qualifier: str
        | t.Callable[[t.Any], t.Mapping] = "get_identity_qualifier",
        get_identity: str | t.Callable[[t.Any, t.Any], t.Mapping] = "get_identity",
        as_dict: str | t.Callable[[t.Any, t.Any], t.Mapping] = "as_dict",
    ):
        self._target_type = target_type
        self._get_identity_qualifier = _unwrap_attr(
            get_identity_qualifier, self._target_type
        )
        self._get_identity = _unwrap_attr(get_identity, self._target_type)
        self._as_dict = _unwrap_attr(as_dict, self._target_type)

    def __call__(self, *args, **kwargs):
        return self._target_type(*args, **kwargs)

    def get_identity_qualifier(self):
        return self._get_identity_qualifier()

    def get_identity(self, item):
        return self._get_identity(item)

    def as_dict(self, item) -> dict:
        return self._as_dict(item)


class AdapterForModel(AdapterForData):
    def __init__(
        self,
        target_type: type,
        get_identity_qualifier: str
        | t.Callable[[t.Any], t.Mapping] = "get_identity_qualifier",
        get_identity: str | t.Callable[[t.Any, t.Any], t.Mapping] = "get_identity",
        as_dict: str | t.Callable[[t.Any, t.Any], t.Mapping] = "as_dict",
        compute_defaults: str | t.Callable[[type], t.Mapping] = "compute_defaults",
    ):
        super().__init__(
            target_type=target_type,
            get_identity_qualifier=get_identity_qualifier,
            get_identity=get_identity,
            as_dict=as_dict,
        )
        self._compute_defaults = _unwrap_attr(compute_defaults, self._target_type)

    def compute_defaults(self):
        return self._compute_defaults()


class BaseDataMapper:
    def __init__(
        self,
        model_type: type,
        data_type: type,
        model_adapter: AdapterForData | None = None,
        data_adapter: AdapterForData | None = None,
    ):
        self.__model_type = model_type
        self.__data_type = data_type
        if not model_adapter:
            model_adapter = AdapterForModel(self.__model_type)
        self._model_adapter = model_adapter
        if not data_adapter:
            data_adapter = AdapterForData(self.__data_type)
        self._data_adapter = data_adapter

    @property
    def model_type(self):
        return self.__model_type

    @property
    def data_type(self):
        return self.__data_type

    def initialize(self, input: dict):
        defaults = self._model_adapter.compute_defaults()
        return self._data_adapter(**(defaults | input))

    def from_model(self, model):
        return self._data_adapter(**self.dump_model(model))

    def to_model(self, data):
        return self._model_adapter(**self.dump_data(data))

    def dump_model(self, model):
        return self._model_adapter.as_dict(model)

    def dump_data(self, data):
        return self._data_adapter.as_dict(data)

    def get_model_identity(self, model):
        return self._model_adapter.get_identity(model)

    def get_data_identity(self, data):
        return self._data_adapter.get_identity(data)

    def get_model_identity_qualifier(self):
        return self._model_adapter.get_identity_qualifier()

    def get_data_identity_qualifier(self):
        return self._data_adapter.get_identity_qualifier()

    def model_to_filter(self, identity_or_model) -> dfs.Eq:
        if isinstance(identity_or_model, self.__model_type):
            identity_or_model = self.get_model_identity(identity_or_model)

        qualifier = self.get_data_identity_qualifier()
        if not isinstance(qualifier, tuple):
            qualifier = (qualifier,)

        filter = dfs.Eq(qualifier[0], identity_or_model)
        return filter


class RequiresDataMapperMixin(require.RequiresMixin, requires="data_mapper"):
    _data_mapper: BaseDataMapper
