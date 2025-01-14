import re

from hazm import Lemmatizer
from meilisearch import Client

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

import registration
from group7.apps import logger
from .forms import UserProfileForm
from .models import Word, FavoriteWord
from .utils import translate_to_farsi

lemmatizer = Lemmatizer()


def get_meilisearch_client():
    return Client('http://127.0.0.1:7700')


def _normalize_query(query: str) -> str:
    suffixes = [' ها', 'ان', ' ها', 'ها', 'ی', 'ي']
    for suffix in suffixes:
        if query.endswith(suffix):
            query = query[:-len(suffix)]
            break
    query = lemmatizer.lemmatize(query)
    query2 = query.split("#")
    query = query2[0]
    return query.strip()


def detect_language(word):
    english_pattern = re.compile(r'^[a-zA-Z]+$')
    return bool(english_pattern.match(word))


def is_user_valid(request):
    sessionid = request.GET.get('sessionid')
    if not sessionid:
        return False
    try:
        session = Session.objects.get(session_key=sessionid)
        session_data = session.get_decoded()
        user_id = session_data.get('_auth_user_id')
        if not user_id:
            return False
    except (Session.DoesNotExist, User.DoesNotExist):
        return False
    return True


def home(request):
    if is_user_valid(request):
        return logout(request)
    return render(request, 'group7.html', {'group_number': '7'})


def about(request):
    return render(request, 'about.html')


def index(request):
    if is_user_valid(request):
        return logout(request)
    return render(request, 'index.html')


def exact_search_wordcard(word):
    try:
        client = get_meilisearch_client()
        index = client.index('words')
        filter_query = f'word = "{word}"'
        results = index.search("", {
            "limit": 1,
            "filter": filter_query,
        })
        return results.get('hits', [])
    except Exception as e:
        logger.exception(f"Unexpected error during search for '{word}': {e}")
        return []


def exact_search_words(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse({"error": "Query parameter 'q' is required."}, status=400)
    try:
        if detect_language(query):
            translation = translate_to_farsi(query)
            response = [{
                "id": None,
                "word": query,
                "synonyms": [translation]
            }]
            return JsonResponse(response, safe=False)
        client = get_meilisearch_client()
        index = client.index('words')
        filter_query = f'word = "{query}"'
        results = index.search("", {
            "limit": 1,
            "filter": filter_query,
        })
        if not results.get('hits', []):
            return search_words(request)
        return JsonResponse(results.get('hits', []), safe=False)
    except Exception:
        logger.exception("Unexpected error during search")
        return JsonResponse({"error": "An unexpected error occurred during the search."}, status=500)


def search_words(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse({"error": "Query parameter 'q' is required."}, status=400)
    query = _normalize_query(query)
    try:
        client = get_meilisearch_client()
        index = client.index('words')
        results = index.search(query, {
            "limit": 1,
        })
        return JsonResponse(results.get('hits', []), safe=False)
    except Exception:
        logger.exception("Unexpected error during search")
        return JsonResponse({"error": "An unexpected error occurred during the search."}, status=500)


def logout(request):
    return registration.views.LogoutPage(request)


def user_profile(request):
    sessionid = request.COOKIES.get('sessionid')
    if not sessionid:
        return logout(request)
    try:
        session = Session.objects.get(session_key=sessionid)
        session_data = session.get_decoded()
        user_id = session_data.get('_auth_user_id')
        if user_id:
            user = User.objects.get(id=user_id)
            favorite_words = FavoriteWord.objects.filter(user=user)
            return render(request, 'profile.html', {'user_data': user, 'favoritewords': favorite_words})
        else:
            return logout(request)
    except (Session.DoesNotExist, User.DoesNotExist):
        return logout(request)


@login_required
def edit_profile(request):
    is_user_valid(request)
    user_profile = request.user.profile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('group7:user_profile')
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'edit_profile.html', {'form': form})


@method_decorator(csrf_exempt, name='dispatch')
def highlight_words(request):
    if request.method == "POST":
        sentence = request.POST.get('sentence', '')
        words_in_sentence = re.findall(r'\b\w+\b', sentence)
        found_words = Word.objects.filter(word__in=words_in_sentence).values_list('word', flat=True)
        return JsonResponse({'words': list(found_words)})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def AddFavoriteWordView(request):
    word = request.POST.get('word')
    if not word:
        return JsonResponse({'error': 'Word parameter is required'}, status=400)
    sessionid = request.COOKIES.get('sessionid')
    if not sessionid:
        return JsonResponse({'error': 'Session ID not found'}, status=400)
    try:
        session = Session.objects.get(session_key=sessionid)
        session_data = session.get_decoded()
        user_id = session_data.get('_auth_user_id')
        user = User.objects.get(id=user_id)
        word_obj = Word.objects.get(word=word)
        favorite, created = FavoriteWord.objects.get_or_create(user=user, word=word_obj)
        if created:
            return JsonResponse({'message': 'Word added to favorites successfully.'}, status=201)
        else:
            return JsonResponse({'message': 'Word is already in favorites.'}, status=200)
    except (Session.DoesNotExist, User.DoesNotExist):
        return JsonResponse({'error': 'Invalid session or user not found'}, status=400)
    except Word.DoesNotExist:
        return JsonResponse({'error': 'Word not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def RemoveFavoriteWordView(request):
    word = request.POST.get('word')
    if not word:
        return JsonResponse({'error': 'Word parameter is required'}, status=400)
    sessionid = request.COOKIES.get('sessionid')
    if not sessionid:
        return JsonResponse({'error': 'Session ID not found'}, status=400)
    try:
        session = Session.objects.get(session_key=sessionid)
        session_data = session.get_decoded()
        user_id = session_data.get('_auth_user_id')
        user = User.objects.get(id=user_id)
        word_obj = Word.objects.get(word=word)
        favorite = FavoriteWord.objects.get(user=user, word=word_obj)
        favorite.delete()
        return JsonResponse({'message': 'Word removed from favorites successfully.'}, status=200)
    except (Session.DoesNotExist, User.DoesNotExist):
        return JsonResponse({'error': 'Invalid session or user not found'}, status=400)
    except Word.DoesNotExist:
        return JsonResponse({'error': 'Word not found'}, status=404)
    except FavoriteWord.DoesNotExist:
        return JsonResponse({'error': 'Word is not in favorites.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def GetFavoriteWordsView(request):
    sessionid = request.COOKIES.get('sessionid')
    if not sessionid:
        return JsonResponse({'error': 'Session ID not found'}, status=400)
    try:
        session = Session.objects.get(session_key=sessionid)
        session_data = session.get_decoded()
        user_id = session_data.get('_auth_user_id')
        user = User.objects.get(id=user_id)
        favorites = FavoriteWord.objects.filter(user=user)
        favorite_words = [favorite.word.word for favorite in favorites]
        return JsonResponse({'favorite_words': favorite_words}, status=200)
    except (Session.DoesNotExist, User.DoesNotExist):
        return JsonResponse({'error': 'Invalid session or user not found'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def wordcard(request, favoriteword):
    result = exact_search_wordcard(favoriteword)
    if result:
        return render(request, 'wordcard.html', {'word': result[0]})
    else:
        return JsonResponse({"error": "No results found for the given word."}, status=404)
