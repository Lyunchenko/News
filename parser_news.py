
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
		not_in_list = False
		try: self._channels.index(url)
		except Exception as e: not_in_list = True
		if not_in_list: self._channels.append(url)

	def del_channel(self, url):
		in_list = True
		try: self._channels.index(url)
		except Exception as e: in_list = False
		if in_list: self._channels.remove(url)


	def start_parse(self):
		links = []
		for url in self._channels:
			links.append([url, None])
		asyncio.run(self._get_news(links, self._handler_rss))

		links = []
		news_list = self._news.get_news()
		for i in news_list:
			links.append([news_list[i]['url'], news_list[i]['id']])
		asyncio.run(self._get_news(links, self._handler_site))

		self._news.save_to_db()


	def _handler_rss(self, url_text, id_news):
		""" Обработка RSS ленты каждого канала"""
		rss_data = feedparser.parse(url_text)
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
					'url': record.link,
					'date': date,
					'description': record.description}
			self._news.set_news(news)


	def _handler_site(self, url_text, id_news):
		""" Получение полного текста новости """
		pass


	async def _get_news(self, links, handler):
		""" Асинхронный запуск списка задач """
		tasks = []
		for l in links:
			tasks.append(asyncio.create_task(self._fetch_async(l[0], handler, l[1])))
		await asyncio.wait(tasks)

	async def _fetch_async(self, url, handler, id_news):
		""" Запрос текста страницы передача в обработчик """
		url_text = await self._aiohttp_get(url)
		handler(url_text, id_news)

	async def _aiohttp_get(self, url):
		""" Получение текста страницы """
		async with aiohttp.ClientSession() as session:
			async with session.get(url) as response:
				return await response.text()



obj = ParserNews()
obj.add_channel('https://news.yandex.ru/business.rss')
#obj.add_channel('https://news.yandex.ru/finances.rss')
#obj.add_channel('https://news.yandex.ru/politics.rss')
obj.start_parse()
