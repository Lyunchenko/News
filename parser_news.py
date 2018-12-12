
import asyncio
import aiohttp
import feedparser
from datetime import datetime
import news


class ParserNews:

	def __init__(self):
		self._channels = []
		self._news = news.News()


	def add_channel(self, url):
		""" Добавление RSS канала в парсер"""
		not_in_list = False
		try: self._channels.index(url)
		except Exception as e: not_in_list = True
		if not_in_list: self._channels.append(url)


	def del_channel(self, url):
		""" Удаленеи RSS канала из парсера"""
		in_list = True
		try: self._channels.index(url)
		except Exception as e: in_list = False
		if in_list: self._channels.remove(url)

	def start_parse(self):
		""" Запуск асинхронной выгрузки новостей из каналов """
		asyncio.run(self.get_news(self._channels, self.handler_rss))
		print(self._news)


	def handler_rss(self, url_text, id_news):
		""" Обработка RSS ленты каждого канала"""
		rss_data = feedparser.parse(rss_text)
		for record in rss_data.entries:
			chek = 'title' in record\
					and 'link' in record\
					and 'description' in record\
					and 'published' in record\
					and 'published_parsed' in record\
					and 'id' in record
			if not chek: continue

			date = record.published_parsed
			date = datetime(date.tm_year, date.tm_mon, date.tm_mday, 
							date.tm_hour, date.tm_min, date.tm_sec)
			news = {'id': record.id,
					'title': record.title,
					'link': record.link,
					'date': date,
					'description': record.description,
					'text': None}
			self._news.set_news(news)

	def handler_site(self, url_text, id_news):
		pass



	async def get_news(self, links, handler, id_news = None):
		""" Асинхронный запуск списка задач """
		tasks = []
		for url in links:
			tasks.append(asyncio.create_task(self.fetch_async(url, handler, id_news)))
		await asyncio.wait(tasks)


	async def fetch_async(self, url, handler, id_news):
		""" Запрос текста страницы передача в обработчик """
		url_text = await self.aiohttp_get(url)
		handler(url_text, id_news)


	async def aiohttp_get(self, url):
		""" Получение текста страницы """
		async with aiohttp.ClientSession() as session:
			async with session.get(url) as response:
				return await response.text()



obj = ParserNews()
obj.add_channel('https://news.yandex.ru/business.rss')
obj.add_channel('https://news.yandex.ru/finances.rss')
obj.add_channel('https://news.yandex.ru/politics.rss')
obj.start_parse()
