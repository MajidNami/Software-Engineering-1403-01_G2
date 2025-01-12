from django.http import JsonResponse
from django.shortcuts import render
from group1.models import PersianWord
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return  render (request , 'group1.html' , {'group_number': '1'})

@login_required
def autocomplete_page(request):
    return render(request, 'autocomplete.html')

# View to return word suggestions in JSON format
def autocomplete_suggestions(request):
    query = request.GET.get('query', '')  # Get the query from the request

    if query:
        # Find Persian words that start with the query string, case-insensitive
        matching_words = PersianWord.objects.filter(word__startswith=query).values_list('word', flat=True)
        suggestions = list(matching_words)
    else:
        suggestions = []

    return JsonResponse({'suggestions': suggestions})