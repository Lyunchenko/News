from news.models import NewsData

class News:

	def __init__(self):
		self._news = {}
		self.field_id = 'title'
		self._list_news = self._get_list_news()
		
	def set_news(self, news):
		""" Добавление новости в словарь"""
		id_news = news[self.field_id]
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
		for key, value in self._news.items():
			add_news = NewsData(
						id_news=value['id'],
						title=value['title'],
						description=value['description'],
						url=value['url'],
						url_ya=value['url_ya'],
						text=value['text'],
						text_html=value['text_html'],
						date=value['date']
						)
			add_news.save()
		self._news = {}

	def _get_list_news(self):
		""" Загрузка списка id последних новостей из базы """
		latest_news_list= NewsData.objects.order_by('-date')[:1000]
		self._list_news = []
		for news in latest_news_list:
			self._list_news.append(getattr(news, self.field_id))
		return(self._list_news)

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