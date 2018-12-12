
import asyncio
import aiohttp
import feedparser
from bs4 import BeautifulSoup
import re
from datetime import datetime
import news


class ParserNews:

	def __init__(self):
		self._channels = []
		self._news = news.News()


	def set_channel(self, url):
		""" Добавление RSS канала Yandex-новости в список обработки"""
		not_in_list = False
		try: self._channels.index(url)
		except Exception as e: not_in_list = True
		if not_in_list: self._channels.append(url)

	def get_channel(self):
		""" Получение списка всех каналов в обработке """
		return(self._channels)

	def del_channel(self, url):
		""" Удаление какнала из списка обработки """
		in_list = True
		try: self._channels.index(url)
		except Exception as e: in_list = False
		if in_list: self._channels.remove(url)


	def start_parse(self):
		""" Запуск процедуры парсинга новостей из каналов"""
		
		# Парсинг даных из новостной ленты yandex
		print('RSS')
		links = []
		for url in self._channels:
			links.append([url, None])
		asyncio.run(self._get_news(links, self._handler_rss))

		# 1 проход - получение настоящих ссылок со страниц яндекса
		# 2 проход - получение полного текста новостей с первоисточника
		tasks = [['url_ya', self._handler_ya],
				 ['url', self._handler_site]]
		for task in tasks:
			print(task[0])
			links = []
			news_list = self._news.get_news()
			for i in news_list:
				links.append([news_list[i][task[0]], news_list[i]['id']])
			asyncio.run(self._get_news(links, task[1]))

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
					'url_ya': record.link,
					'date': date,
					'description': record.description}
			self._news.set_news(news)


	def _handler_ya(self, url_text, id_news):
		""" Получение ссылок на исходные статьи со страниц яндекса """
		soup = BeautifulSoup(url_text, 'lxml')
		url = soup.find(attrs={'class':'doc__content'}).find('a')['href']
		self._news.set_attribute(id_news, 'url', url)

	def _handler_site(self, url_text, id_news):
		""" Получение всего текста новостей"""
		self._news.set_attribute(id_news, 'text_html', url_text)
		text = self._parse_site(id_news, url_text)
		self._news.set_attribute(id_news, 'text', text)


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


	def _parse_site(self, id_news, url_text):
		""" Парсинг html страицы с новостью"""
		soup = BeautifulSoup(url_text, 'lxml')
		# Описание новости из rss должно встречаться в исходной статье
		# Разбиваем описание на несколько частей т.к. можно стлнуться с ссылками по тексту
		description = self._news.get_attribute(id_news, 'description')
		cut = int(len(description)/4)
		tasks = [description, description[:-cut], description[cut:],
				 description[:cut*2], description[cut*2:],
				 description[cut:], description[cut:cut*2], 
				 description[cut*2:cut*3], description[cut*3:]]
		for task in tasks:
			try: 
				text = soup.find(text=re.compile(task)).parent.parent.text
			except Exception as e: 
				text = None
			if text != None: return(text)


obj = ParserNews()
obj.set_channel('https://news.yandex.ru/business.rss')
#obj.set_channel('https://news.yandex.ru/finances.rss')
#obj.set_channel('https://news.yandex.ru/politics.rss')
obj.start_parse()
