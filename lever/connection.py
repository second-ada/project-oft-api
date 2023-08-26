import sqlite3


class Connection:
	path = None
	conn = None
	cursor = None

	@classmethod
	def load_database(cls, path):
		cls.path = path

	@classmethod
	def get_connection(cls):
		if not cls.conn:
			cls.conn = sqlite3.connect(cls.path, check_same_thread=False)
			cls.cursor = cls.conn.cursor()
		
		return cls.conn, cls.cursor
