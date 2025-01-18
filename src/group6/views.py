import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from transformers import pipeline
import hazm

FEEDBACK_FILE = "group6/system_feedback.json"
GENERATED_TEXTS_DIR = "generated_texts"

normalizer = hazm.Normalizer(persian_numbers=False)
generator = pipeline('text-generation', "./group6/gpt2-fa")


def normalize_input(text):
    text = normalizer.normalize(text)
    return text


def sents_as_output(text, num_sents=1):
    sents = hazm.sent_tokenize(text)
    if num_sents > 0:
        return " ".join(sents[:num_sents])
    return " ".join(sents[0])


def count_words(text):
    words = hazm.word_tokenize(text)
    return len(words)


def load_feedback():
    try:
        with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"ratings": [], "average": 0}


def save_feedback(feedback_data):
    with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
        json.dump(feedback_data, f, ensure_ascii=False, indent=4)


def home(request):
    return render(request, "home.html")


def suggest_word(request):
    text = request.GET.get("text", "").strip()
    text = normalize_input(text)

    outputs = generator(text, max_new_tokens=1, num_return_sequences=20)
    unique_suggestions = set()

    for output in outputs:
        generated = output["generated_text"]
        last_word = sents_as_output(generated).split()[-1]
        if text.split()[-1] in last_word:
            continue
        unique_suggestions.add(last_word)
        if len(unique_suggestions) == 3:
            break

    suggestions = list(unique_suggestions)
    return JsonResponse({"suggestions": suggestions})


def system_feedback(request):
    rating = int(request.GET.get("rating", 0))
    feedback_data = load_feedback()

    feedback_data["ratings"].append(rating)
    total_ratings = len(feedback_data["ratings"])
    feedback_data["average"] = sum(feedback_data["ratings"]) / total_ratings

    save_feedback(feedback_data)
    return JsonResponse({
        "message": "بازخورد شما با موفقیت ثبت شد.",
        "average_rating": feedback_data["average"]
    })


def download_text(request):
    text = request.GET.get("text", "").strip()
    if not text:
        return JsonResponse({"error": "متن خالی است."})

    response = HttpResponse(text, content_type='text/plain;charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="generated_text.txt"'
    return response
