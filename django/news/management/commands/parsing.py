from django.core.management.base import BaseCommand
import schedule
import time
from news.app.parser_news import ParserNews
from news.models import Channels



class Command(BaseCommand):
    """ Запуск скрипта выполняющего периодический парсинг новостей """
    def handle(self, *args, **options):

        obj_parsing = ParserNews()

        # Додавление каналов из базы
        channels = Channels.objects.all()
        print('\nAdd channels:')
        for channel in channels:
            obj_parsing.set_channel(channel.url)
            print(channel.url)

        # Запуск
        schedule.every(1).minutes.do(obj_parsing.start_parse).tag('tasks', 'friend')
        print('\nQuit the parsing with CTRL-BREAK\n')
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            schedule.clear('tasks')
   
        