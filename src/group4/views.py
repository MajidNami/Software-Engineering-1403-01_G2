from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from src.group4.logic.miss_spell_finder import SpellCorrector


def home(request):
    return render(request, 'index.html', {'group_number': '5'})


@api_view(['POST'])
def handle_text_request(request):
    data = request.data
    text = data.get('text')
    spell_corrector = SpellCorrector()
    result = spell_corrector.miss_spell_suggestion(text)
    wrong_words = []
    for item in result:
        for wrong_word, suggestions in item.items():
            wrong_words.append([wrong_word, suggestions])

    response_data = {
        "wrongWords": wrong_words
    }
    return Response(response_data)


@api_view(['POST'])
def handle_file_upload(request):
    uploaded_file = request.FILES.get('file')
    if not uploaded_file:
        return Response({"error": "No file was uploaded."}, status=400)

    try:
        file_content = uploaded_file.read().decode('utf-8')
        spell_corrector = SpellCorrector()
        result = spell_corrector.miss_spell_suggestion(file_content)
        formatted_result = {
            "wrongWords": [
                {"wrongWord": wrong_word, "suggestions": suggestions}
                for item in result
                for wrong_word, suggestions in item.items()
            ],
            "text": file_content
        }
        return JsonResponse(formatted_result, safe=False)

    except Exception as e:
        return Response({"error": str(e)}, status=500)

