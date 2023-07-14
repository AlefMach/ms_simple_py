from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

POSTGRES_INDEXES_NAMING_CONVENTION = {
    'ix': '%(column_0_label)s_idx',
    'uq': '%(table_name)s_%(column_0_name)s_key',
    'ck': '%(table_name)s_%(constraint_name)s_check',
    'fk': '%(table_name)s_%(column_0_name)s_fkey',
    'pk': '%(table_name)s_pkey',
}
metadata = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)


class BaseModel(DeclarativeBase):
    metadata = metadata

    def __repr__(self) -> str:
        columns = ', '.join([f'{k}={repr(v)}' for k, v in self.__dict__.items() if not k.startswith('_')])
        return f'<{self.__class__.__name__}({columns})>'
