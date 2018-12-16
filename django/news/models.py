from django.db import models


class Channels(models.Model):
    url = models.CharField(max_length=200)
    
    def __str__(self):
        return self.url

class ChoiceIndex(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class ChoiceType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class NewsData(models.Model):
    id_news = models.TextField()
    title = models.TextField()
    description = models.TextField()
    url = models.TextField()
    url_ya = models.TextField()
    text = models.TextField(null=True)
    text_html = models.TextField()
    date = models.DateTimeField()
    choice_index = models.ForeignKey(ChoiceIndex, 
                                     on_delete=models.PROTECT, 
                                     null=True, blank=True)
    choice_type = models.ForeignKey(ChoiceType, 
                                    on_delete=models.PROTECT, 
                                    null=True, blank=True)

    def __str__(self):
        return self.title

