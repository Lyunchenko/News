from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.db.models import Q
from .models import NewsData, ChoiceIndex, ChoiceType



def index(request):
	news_list = NewsData.objects.filter(Q(choice_index=None) 
									    | Q(choice_type=None))
	context = {'news_list': news_list}
	return render(request, 'news/index.html', context)


def detail(request, news_id):
	news = get_object_or_404(NewsData, pk=news_id)
	
	# Список идексов для выбора
	choice_index = ChoiceIndex.objects.all()
	index_var = []
	for choice in choice_index:
		if choice == news.choice_index: checked = 'checked'
		else: checked = ''
		index_var.append({
			'id': choice.id,
			'name': choice.name,
			'checked': checked
			})

	# Список типов прогнозов
	choice_type = ChoiceType.objects.all()
	type_var = []
	for choice in choice_type:
		if choice == news.choice_type: checked = 'checked'
		else: checked = ''
		type_var.append({
			'id': choice.id,
			'name': choice.name,
			'checked': checked
			})

	data = {'news': news, 
			'index_var': index_var,
			'type_var': type_var}
	return render(request, 'news/detail.html', data)


def choice(request, news_id):

	news = get_object_or_404(NewsData, pk=news_id)
	
	try:
		choice_index = get_object_or_404(ChoiceIndex, pk=request.POST['index'])
		news.choice_index = choice_index
	except Exception as e:
		pass

	try:
		choice_type = get_object_or_404(ChoiceType, pk=request.POST['type'])
		news.choice_type = choice_type
	except Exception as e:
		pass

	news.save()

	return HttpResponseRedirect(reverse('news:index'))