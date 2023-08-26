import typing
from math import ceil
from random import randint
from .connection import Connection


class ColumnTypes:
    INTEGER = 'INTEGER'
    TEXT = 'TEXT'

    @classmethod
    def get_types(cls):
        return [cls.INTEGER, cls.TEXT]


def Column(
    field: str,
    typ: str,
    primary_key: bool = False,
    autoincrement: bool = False,
    unique: bool = False,
    nullable: bool = True,
    default: typing.Any = None
) -> str:

    sttm = [field, typ]

    if primary_key:
        sttm.append('PRIMARY KEY')

    if autoincrement:
        sttm.append('AUTOINCREMENT')

    if unique:
        sttm.append('UNIQUE')

    if nullable is False:
        sttm.append('NOT NULL')

    if default is not None:
        sttm.append(f'DEFAULT {default}')

    return ' '.join(sttm)


class Pagination:

    def __init__(
        self, page: int, per_page: int, pages: int, items: list,
        total_items: int
    ):
        self.page = page
        self.per_page = per_page
        self.pages = pages
        self.items = items
        self.total_items = total_items

    def json(self):
        return {
            'results': [model.__json__() for model in self.items],
            'page': self.page,
            'pages': self.pages,
            'per_page': self.per_page,
            'total': self.total_items
        }

    def __repr__(self):
        return (
            f'<Pagination page="{self.page}" per_page="{self.per_page}" '
            f'pages="{self.pages}" items="..." total_items="{self.total_items}">'
        )


class Model:
    __table__: str = None
    primary_key: str = None
    fields: list = []

    def __init__(self, **data):
        self.conn, self.cursor = Connection.get_connection()

        self._select = ['*']
        self._where = []
        self._order_by = self.primary_key
        self._limit = None
        self._offset = None
        self._data = {}

        if self.__table__ is None:
            self.__table__ = self.__class__.__name__.lower().rstrip('s') + 's'

        if self.primary_key not in data.items():
            setattr(self, self.primary_key, None)

        for key, value in data.items():
            if key in self.fields:
                setattr(self, key, value)

    def __json__(self, excludes: list = []):
        excludes = ['conn', 'cursor', 'primary_key', 'fields'] + excludes
        attrs = {
            key: value
            for key, value in self.__dict__.items() if not callable(value)
            and not key.startswith('_') and key not in excludes
        }

        return attrs

    def __model__(self, data: tuple):
        if not data:
            return None

        fields = self._select

        if fields == ['*']:
            fields = self.fields

        model = self.__class__()

        for key, value in zip(fields, data):
            setattr(model, key, value)

        return model

    def _get_primary_key(self):
        return self.__json__().get(self.primary_key)

    def select(self, fields: typing.Union[list[str], str] = None):
        if type(fields) == str:
            fields = [field.strip() for field in fields.split(',')]

        if fields is not None:
            self._select = [self.primary_key] + fields

        return self

    def where(self, key: str, value: any, op: str = '='):
        prefix = 'WHERE'
        unique_key = f'{key}_{randint(1, 100)}'

        if len(self._where) > 0:
            prefix = 'AND'

        self._where.append(f'{prefix} {key} {op} :{unique_key}')
        self._data[unique_key] = value

        return self

    def or_where(self, key: str, value: any, op: str = '='):
        prefix = 'WHERE'
        unique_key = f'{key}_{randint(1, 100)}'

        if len(self._where) > 0:
            prefix = 'OR'

        self._where.append(f'{prefix} {key} {op} :{unique_key}')
        self._data[unique_key] = value

        return self

    def order_by(self, order: str):
        self._order_by = order
        return self

    def limit(self, limit: int = None):
        if type(limit) != int:
            raise Exception('Limit method only acepts integer.')

        self._limit = limit
        return self

    def offset(self, offset: int = None):
        if type(offset) != int:
            raise Exception('Limit method only acepts integer.')

        self._offset = offset
        return self

    def _prepare(self):
        select = ', '.join(self._select)
        query = f'SELECT {select} FROM {self.__table__}'

        if len(self._where) > 0:
            query += ' ' + ' '.join(self._where)

        if self._order_by is not None:
            query += f' ORDER BY {self._order_by}'

        if self._limit is not None:
            query += f' LIMIT {self._limit}'

        if self._offset is not None:
            query += f' OFFSET {self._offset}'

        self.query = query
        self.cursor.execute(query, self._data)

    def save(self):
        data = self.__json__()

        keys = ', '.join(data.keys())
        placeholders = ', '.join([f':{key}' for key in data.keys()])

        query = f'INSERT INTO {self.__table__} ({keys}) VALUES ({placeholders})'

        self.cursor.execute(query, data)
        return self

    def delete(self):
        primary_key = self._get_primary_key()

        query = f'DELETE FROM {self.__table__} WHERE {self.primary_key} = ?'

        self.cursor.execute(query, [primary_key])
        return self

    def count(self):
        query = f'SELECT COUNT(*) from {self.__table__}'

        if len(self._where) > 0:
            query += ' ' + ' '.join(self._where)

        res = self.cursor.execute(query, self._data).fetchone()

        return res[0] if res is not None else 0

    def commit(self):
        self.conn.commit()
        return self.cursor.lastrowid

    def first(self):
        self._prepare()

        res = self.cursor.fetchone()
        return self.__model__(res)

    def get_all(self):
        self._prepare()

        res = self.cursor.fetchall()
        return [self.__model__(item) for item in res]

    def paginate(self, page: int = 1, per_page: int = 20):
        self.limit(per_page)
        self.offset((page - 1) * per_page)

        total = self.count()

        self._prepare()

        return Pagination(
            page=page,
            per_page=per_page,
            pages=ceil(total / per_page),
            items=self.get_all(),
            total_items=total
        )
