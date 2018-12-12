


class News:

	def __init__(self):
		self._news = {}

	def set_news(self, news):
		""" Добавление новости в словарь """
		id_news = news['id']
		if not id_news in self._news: 
			news.pop('id')
			self._news[id_news] = news

