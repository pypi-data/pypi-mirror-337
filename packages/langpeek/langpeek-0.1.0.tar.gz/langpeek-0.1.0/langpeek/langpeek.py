import yaml
import os


def _load_stopwords():
    data_path = os.path.join(os.path.dirname(os.__file__), "site-packages", "langpeek", "data", "stopwords.yaml")
    with open(data_path, "r", encoding="utf-8") as f:
        return yaml.load(f, Loader=yaml.Loader)

STOPWORDS = _load_stopwords()

def detect_language(text):
    text = text.lower()
    words = set(text.split())
    scores = {}

    for lang, stopwords in STOPWORDS.items():
        common = words & set(stopwords)
        scores[lang] = len(common)

    best_match = max(scores, key=scores.get)
    return best_match