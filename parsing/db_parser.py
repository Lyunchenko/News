from abc import ABC, abstractmethod
import psycopg2
import datetime


class DBParser:

	def __init__(self, type_db='sqlite'):
		if type_db=='sqlite': self.db = SQLite()
		elif type_db=='postgresql': self.db = PostgreSQL()

	def get_list_news(self):
		return([])

	def set_news(self, news):
		pass



class DB(ABC):

	@abstractmethod
	def get_list_news(self):
		return([])

	@abstractmethod
	def set_news(self, news):
		pass



class SQLite:

    def __init__(self):
        pass


class PostgreSQL:

	def __init__(self):
		# Создание подключения к БД
		self.connect_db = psycopg2.connect(
							dbname='News', 
							user='admin', 
							password='admin')
		# Проверка наличия таблицы news, создание таблицы
		cursor = self.connect_db.cursor()
		cursor.execute("select * from information_schema.tables where table_name=%s", 
						('news_newsdata',))
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



'''
BEGIN;
--
-- Create model ChoiceIndex
--
CREATE TABLE "news_choiceindex" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT
, "name" varchar(200) NOT NULL);
--
-- Create model ChoiceType
--
CREATE TABLE "news_choicetype" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
 "name" varchar(200) NOT NULL);
--
-- Create model News
--
CREATE TABLE "news_news" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "id_n
ews" text NOT NULL, "title" text NOT NULL, "description" text NOT NULL, "url" te
xt NOT NULL, "url_ya" text NOT NULL, "text" text NOT NULL, "text_html" text NOT
NULL, "date" datetime NOT NULL, "choice_index_id" integer NOT NULL REFERENCES "n
ews_choiceindex" ("id") DEFERRABLE INITIALLY DEFERRED, "choice_type_id" integer
NOT NULL REFERENCES "news_choicetype" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE INDEX "news_news_choice_index_id_e04a3bbe" ON "news_news" ("choice_index_
id");
CREATE INDEX "news_news_choice_type_id_dd92f9a6" ON "news_news" ("choice_type_id
");
COMMIT;

'''