def polarity():
    return [
        """
        from textblob import TextBlob

        sentence = "The quick brown fox jumps over the lazy dog."

        blob = TextBlob(sentence)

        polarity = blob.sentiment.polarity

        if polarity > 0:
            print("Positive Sentiment")
        elif polarity < 0:
            print("Negative Sentiment")
        else:
            print("Neutral Sentiment")

        print(f"Polarity Score: {polarity :.2f}")
        """
    ]