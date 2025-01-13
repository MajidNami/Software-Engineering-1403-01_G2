from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.group5.hashem.draft import spell_corrector


def home(request):
    return render(request, 'index.html', {'group_number': '5'})


@api_view(['POST'])
def handle_text_request(request):
    data = request.data
    text = data.get('text')
    dataset_name = data.get('dataset_name', 'fa')
    print(text)
    print(dataset_name)
    result = spell_corrector(text)
    print(result)
    wrong_words = []
    for item in result:
        for wrong_word, suggestions in item.items():
            wrong_words.append([wrong_word, suggestions])

    response_data = {
        "wrongWords": wrong_words
    }
    return Response(response_data)

#
# @api_view(['GET'])
# def suggest_word_api(request):
#     text = request.GET.get('text', '')
#     dataset_name = request.GET.get('dataset', 'fa')
#     suggestion = ngram_model.suggest_word(text, dataset_name)
#     return Response({'suggestions': suggestion})
