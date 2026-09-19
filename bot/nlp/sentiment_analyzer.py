from transformers import pipeline


def load_sentiment_model():
    return pipeline(
        task='sentiment-analysis',
        model='blanchefort/rubert-base-cased-sentiment'
    )


sentiment_analyzer = load_sentiment_model()


def analyze_review(text: str) -> dict:
    result = sentiment_analyzer(text)[0]
    return {
        "label": result["label"],
        "score": result["score"]
    }
