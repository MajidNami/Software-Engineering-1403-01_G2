import json
from django.http import JsonResponse
from django.shortcuts import render

from transformers import pipeline
import hazm

SCORES_FILE = "word_scores.json"

def load_scores():
    try:
        with open(SCORES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_scores(scores):
    with open(SCORES_FILE, "w", encoding="utf-8") as f:
        json.dump(scores, f, ensure_ascii=False, indent=4)

def home(request):
    return render(request, "home.html")



normalizer = hazm.Normalizer(persian_numbers=False)

def normalize_input(text):
    text = normalizer.normalize(text)
    return text

def sents_as_output(text, num_sents=1):
    sents = hazm.sent_tokenize(text)
    if num_sents > 0:
        return " ".join(sents[:num_sents])
    return " ".join(sents[0])

generator = pipeline('text-generation', "./group6/gpt2-fa")


def count_words(text):
    words = hazm.word_tokenize(text)
    return len(words)

def suggest_word(request):
    scores = load_scores()
    text = request.GET.get("text", "").strip()

    text = normalize_input(text)
    print(count_words(text))
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
    print(suggestions)

    last_word = text.split()[-1] if text else ""
    suggestion_scores = {word: scores.get(word, 0) for word in suggestions}
    return JsonResponse({"suggestions": suggestions, "scores": suggestion_scores})

def rate_word(request):
    word = request.GET.get("word", "").strip()
    rating = int(request.GET.get("rating", 0))
    scores = load_scores()

    if word:
        scores[word] = scores.get(word, 0) + rating
        save_scores(scores)
        return JsonResponse({"message": f"امتیاز برای '{word}' ثبت شد.", "new_score": scores[word]})
    return JsonResponse({"message": "کلمه نامعتبر است."})
