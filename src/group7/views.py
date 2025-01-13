from django.http import JsonResponse
from django.shortcuts import render
import logging
from hazm import *
from meilisearch import Client

from group7.apps import logger


# Create your views here.

def home(request):
    return render (request , 'group7.html' , {'group_number': '7'})



def about(request):
    return render (request , 'about.html' )

def index(request):
    return render (request , 'index.html')




def get_meilisearch_client():
    return Client('http://127.0.0.1:7700')


def _normalize_query(query: str) -> str:
    suffixes = [' ها', 'ان', ' ها', 'ها','ی', 'ي', ]
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

