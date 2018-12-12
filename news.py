
import db_parser


class News:

	def __init__(self):
		self._news = {}
		self._db = db_parser.DBParser() 
		self._get_list_news()


	def set_news(self, news):
		""" Добавление новости в словарь"""
		id_news = news['id']
		if self._chek_add_id(id_news): 
			self._news[id_news] = news

	def get_news(self):
		""" Получение списка новостей"""
		return(self._news)

	def set_attribute(self, id_news, attribute, value):
		""" Добавление/изменение аттрибута новости """
		self._news[id_news][attribute] = value

	def get_attribute(self, id_news, attribute):
		""" Получение аттрибута новости """
		return(self._news[id_news][attribute])

	def save_to_db(self):
		""" Сохранение всех новостей в базу днных"""
		self._db.set_news(self._news)
		self._news = {}

	def _get_list_news(self):
		""" Загрузка списка id последних новостей из базы """
		self._list_news = self._db.get_list_news()

	def _chek_add_id(self, id_news):
		""" Проверка наличия новости и добавление ее в список проверки """
		not_in_list = False
		try: self._list_news.index(id_news)
		except Exception as e: not_in_list = True
		if not_in_list: self._list_news.append(id_news)
		self._chek_list_size
		return(not_in_list)

	def _chek_list_size(self):
		"""Удаление старых новостей из списка проверки"""
		if len(self._list_news)>=1100:
			self._list_news = self._list_news[-1000:]