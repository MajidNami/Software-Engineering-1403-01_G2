from googletrans import Translator

def translate_to_farsi(word):
    translator = Translator()
    try:
        translated = translator.translate(word, src='en', dest='fa')
        return translated.text
    except Exception as e:
        return f"Error: {e}"
