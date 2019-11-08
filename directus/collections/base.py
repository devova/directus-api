import re
from dataclasses import dataclass
from functools import partial
from typing import Any

from directus.collections.registry import REGISTRY


@dataclass
class Field(object):
    type: str
    options: dict = None
    auto_increment: bool = False
    datatype: str = "VARCHAR"
    default_value: Any = None
    group: str = ''
    hidden_browse: bool = False
    hidden_detail: bool = False
    id: int = None
    interface: str = 'text-input'
    length: int = 255
    locked: bool = 0
    note: str = ''
    primary_key: bool = False
    readonly: bool = False
    required: bool = False
    signed: bool = True
    sort: int = None
    translation: str = ''
    unique: bool = False
    validation: str = None
    width: str = 'full'


IdField = partial(Field, type='integer', datatype='INT', interface='primary-key', length=10, primary_key=True,
                  required=True, auto_increment=True, hidden_browse=True, hidden_detail=True, sort=0)

StringField = partial(Field, type='string', datatype='VARCHAR', interface='text-input', length=255)


def camel_to_snake_case(value: str) -> str:
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', value)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


class Registry(type):

    def __new__(cls, clsname, bases, attrs):
        klass = super().__new__(cls, clsname, bases, attrs)
        klass._meta = klass.Meta()
        klass._meta.collection = camel_to_snake_case(klass.__name__)
        if bases:
            REGISTRY[klass._meta.collection] = klass
        return klass


class Meta:
    collection: str
    note: str = None
    hidden: bool = False
    single: bool = False
    managed: bool = True
    icon: str = 'folder_open'
    translation: str = None


class Collection(metaclass=Registry):
    id = IdField()

    class Meta(Meta):
        pass

    def __init__(self, **kwargs):
        for field in self.fields():
            setattr(self, field, kwargs.get(field) or getattr(self.__class__, field).default_value)

    @classmethod
    def fields(cls):
        return [field for field in dir(cls) if isinstance(getattr(cls, field), Field)]

    @classmethod
    def fields_info(cls):
        fields_info = []
        for field in cls.fields():
            field_info = dict(getattr(cls, field).__dict__)
            field_info['collection'] = cls._meta.collection
            field_info['field'] = field
            fields_info.append(field_info)
        return fields_info

    @classmethod
    def info(cls):
        return {
            'collection': cls._meta.collection,
            'note': cls._meta.note,
            'hidden': cls._meta.hidden,
            'single': cls._meta.single,
            'managed': cls._meta.managed,
            'fields': {info['field']: info for info in cls.fields_info()},
            'icon': cls._meta.icon,
            'translation': cls._meta.translation
        }

    @classmethod
    def items(cls, scope):
        raise NotImplementedError(
            f'Collection `{cls.__name__}/{cls.Meta.collection}` has not implemented `items()` method')

    @classmethod
    def create(cls, data: dict):
        raise NotImplementedError

    @classmethod
    def get(cls, id: int):
        raise NotImplementedError

    @classmethod
    def update(cls, id: int, data: dict):
        raise NotImplementedError

    @classmethod
    def delete(cls, id: int):
        raise NotImplementedError
