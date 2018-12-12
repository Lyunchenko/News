
import psycopg2
import datetime

class DBParser:

	def __init__(self):
		# Создание подключения к БД
		self.connect_db = psycopg2.connect(
							dbname='News', 
							user='admin', 
							password='admin')
		# Проверка наличия таблицы news, создание таблицы
		cursor = self.connect_db.cursor()
		cursor.execute("select * from information_schema.tables where table_name=%s", ('news',))
		answer = bool(cursor.rowcount)
		cursor.close()
		if not answer:
			self._create_table_news()


	def __del__(self):
 		self.connect_db.close()


	def get_list_news(self):
		""" Получение списка id новостей за последние 2 суток """
		date = datetime.datetime.today()-datetime.timedelta(days=2)
		sql = '''SELECT news.id
                 FROM news
                 WHERE news.date >= %s;
              '''
		data = self.get_sql(sql, (date, ))
		return(data)

	def set_news(self, news):
		"""Добавление новостей в базу"""
		sql = f'INSERT INTO tripdata VALUES ({("%s,"*17)[:-1]});'
		cursor = self.connect_db.cursor()
		for key, value in news.items():
			line_data = [value['id'],
						 value['title'],
						 value['url_ya'],
						 value['date'],
						 value['description'],
						 value['text_html'],
						 value['text'],
						 value['url']]
			cursor.execute(sql, line_data)
		cursor.close()
		self.connect_db.commit()


	def _create_table_news(self):
		""" Создание таблицы с новостями """
		columns = { 'id': 'varchar PRIMARY KEY',
					'title': 'varchar',
					'url_ya': 'varchar',
					'date': 'timestamp',
					'description': 'varchar',
					'text_html': 'varchar',
					'text': 'varchar',
					'url': 'varchar'}
		self._create_table('news', columns)


	def _create_table(self, table_name, columns):
		# Формирование SQL
		parameters = ''
		for key, value in columns.items():
			if parameters!='': parameters +=','
			parameters += key + ' ' + value
		sql = f'CREATE TABLE {table_name} ({parameters});'
		# Исполнение SQL
		cursor = self.connect_db.cursor()
		cursor.execute(sql, parameters)
		cursor.close()
		self.connect_db.commit()

	def _get_sql(self, sql, parameters):
		cursor = self.connect_db.cursor()
		cursor.execute(sql, parameters)
		data = cursor.fetchall()   
		cursor.close()
		return(data)