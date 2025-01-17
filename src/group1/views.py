from django.http import JsonResponse
from django.shortcuts import render
from group1.models import PersianWord
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt



def home(request):
    return render(request, 'group1.html', {'group_number': '1'})


@login_required
def autocomplete_page(request):
    return render(request, 'autocomplete.html')


@login_required
def autocomplete_suggestions(request):
    query = request.GET.get('query', '').strip()
    
    if query:
        
        last_word = query.split()[-1]  #last word of the query

        #find Persian words that start with the last word and order by frequency
        matching_words = (
            PersianWord.objects.filter(word__startswith=last_word)
            .order_by('-frequency')
            .values_list('word', flat=True)
        )
        suggestions = list(matching_words)
    else:
        suggestions = []

    return JsonResponse({'suggestions': suggestions})

def update_frequency(request):
    if request.method == 'POST':
        print("Update frequency endpoint triggered")
        try:
            import json
            print("Raw request body:", request.body)
            data = json.loads(request.body)
            print("Parsed JSON data:", data)
            word = data.get('word')
            print("Received word:", word)
            if word:
                #update frequency or create the word if it doesn't exist
                word_obj, created = PersianWord.objects.get_or_create(word=word)
                print("Selected Word:", word_obj.word, "Frequency:", word_obj.frequency)
                word_obj.frequency += 1
                print("After update Frequency:", word_obj.frequency)
                word_obj.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Word not provided'}, status=400)
        except Exception as e:
            print("Exception occurred:", str(e))
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    print("Invalid request method")
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)



#not important
def test_word_frequency(request, word):
    """
    Test function to get the frequency of a given word.
    """
    try:
        persian_word = PersianWord.objects.filter(word=word).first()
        
        if persian_word:
            return JsonResponse({
                'word': persian_word.word,
                'frequency': persian_word.frequency
            })
        else:
            return JsonResponse({
                'error': 'Word not found in the database.'
            })
    except Exception as e:
        return JsonResponse({
            'error': f'An error occurred: {str(e)}'
        })
