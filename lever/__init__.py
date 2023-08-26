from .connection import Connection
from .model import Model, Column, ColumnTypes
from .migration import Migration

class Database:
	def __init__(self, path):
		Connection.load_database(path)

		self.conn, self.cursor = Connection.get_connection()

		self.__add_model_attrs()
		self.Migration = Migration

	def __add_model_attrs(self):
		self.Model = Model
		self.Column = Column
		
		for type_in in ColumnTypes.get_types():
			setattr(self, type_in, type_in)

	def create_table(self, table: str, fields: list):
		fields_sttm = ', '.join(fields)
		query = f'CREATE TABLE IF NOT EXISTS {table} ({fields_sttm})'

		self.cursor.execute(query)

	def drop_table(self, table: str):
		query = f'DROP TABLE IF EXISTS {table}'

		self.cursor.execute(query)

	def tables(self):
		query = (
			"SELECT name FROM sqlite_schema "
			"WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
		)

		data = self.cursor.execute(query).fetchall()
		return [item[0] for item in data]
