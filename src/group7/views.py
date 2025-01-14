from django.http import JsonResponse
from django.shortcuts import render
import logging
from hazm import *
from meilisearch import Client
from .utils import translate_to_farsi
from group7.apps import logger


# Create your views here.

def home(request):
    return render(request, 'group7.html', {'group_number': '7'})


def about(request):
    return render(request, 'about.html')


def index(request):
    return render(request, 'index.html')


def get_meilisearch_client():
    return Client('http://127.0.0.1:7700')


def _normalize_query(query: str) -> str:
    suffixes = [' ها', 'ان', ' ها', 'ها', 'ی', 'ي', ]
    for suffix in suffixes:
        if query.endswith(suffix):
            query = query[:-len(suffix)]
            break

    query = lemmatizer.lemmatize(query)
    query2 = query.split("#")
    query = query2[0]

    return query.strip()


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
        print(results.get('hits', []))
        return JsonResponse(results.get('hits', []), safe=False)

    except Exception as e:
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

    except Exception as e:
        logger.exception("Unexpected error during search")
        return JsonResponse({"error": "An unexpected error occurred during the search."}, status=500)


from django.http import JsonResponse
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.shortcuts import render


def user_profile(request):
    sessionid = request.COOKIES.get('sessionid')

    if not sessionid:
        return JsonResponse({'error': 'Session ID not found'}, status=400)

    try:

        session = Session.objects.get(session_key=sessionid)
        session_data = session.get_decoded()

        user_id = session_data.get('_auth_user_id')

        if user_id:

            user = User.objects.get(id=user_id)

            return render(request, 'profile.html', {'user_data': user})
        else:
            return JsonResponse({'error': 'User not found in session'}, status=400)

    except Session.DoesNotExist:
        return JsonResponse({'error': 'Invalid session ID'}, status=400)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=400)


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm


@login_required
def edit_profile(request):
    user_profile = request.user.profile  # دسترسی به پروفایل کاربر
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('group7:user_profile')
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'edit_profile.html', {'form': form})


import re


def detect_language(word):
    english_pattern = re.compile(r'^[a-zA-Z]+$')

    if english_pattern.match(word):
        return True

    else:
        return False
