
import pandas

class News:

	def __init__(self):
		self._news = {}
		self._db = None 
		self._get_list_news()


	def set_news(self, news):
		id_news = news['id']
		if self._chek_add_id(id_news): 
			self._news[id_news] = news

	def get_news(self):
		return(self._news)

	def update_news(self, id_news, attribute, value):
		self._news[id_news][attribute] = value

	def save_to_db(self):
		df = pandas.DataFrame(self._news).T
		df.to_csv('data.csv', sep=';')
		self._news = {}


	def _get_list_news(self):
		""" Загрузка списка id последних новостей из базы """
		self._list_news = []
		pass

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