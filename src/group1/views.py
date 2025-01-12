from django.http import JsonResponse
from django.shortcuts import render
from group1.models import PersianWord
from django.contrib.auth.decorators import login_required

# Home view for group1
def home(request):
    return render(request, 'group1.html', {'group_number': '1'})

# Autocomplete page view
@login_required
def autocomplete_page(request):
    return render(request, 'autocomplete.html')

# AJAX endpoint to return word suggestions
@login_required
def autocomplete_suggestions(request):
    query = request.GET.get('query', '').strip()  # Get the query and remove extra spaces
    
    if query:
        # Isolate the last word in the input
        last_word = query.split()[-1]  # Get the last word of the query
        # Find Persian words that start with the last word
        matching_words = PersianWord.objects.filter(word__startswith=last_word).values_list('word', flat=True)
        suggestions = list(matching_words)
    else:
        suggestions = []

    return JsonResponse({'suggestions': suggestions})
