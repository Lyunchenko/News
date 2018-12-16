from django.urls import path

from . import views

app_name = 'news'
urlpatterns = [
	# ex: /news/
    path('', views.index, name='index'),
    # ex: /news/5/
    path('<int:news_id>/', views.detail, name='detail'),
    # ex: /news/5/choice/
    path('<int:news_id>/choice/', views.choice, name='choice'),
]