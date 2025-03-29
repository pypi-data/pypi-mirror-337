def rule():
    return [
        """
        positive_words = ['good', 'happy', 'joyful', 'excellent', 'love', 'amazing', 'great', 'positive']
        negative_words = ['bad', 'sad', 'angry', 'horrible', 'hate', 'terrible', 'awful', 'negative']

        def sentiment_analysis(sentence):
            words = sentence.lower().split()

            positive_count = 0
            negative_count = 0

            for word in words:
                if word in positive_words:
                    positive_count += 1
                elif word in negative_words:
                    negative_count += 1

            if positive_count > negative_count:
                return "Positive Sentiment"
            elif negative_count > positive_count:
                return "Negative Sentiment"
            else:
                return "Neutral Sentiment"

        sentence = input("Enter a sentence: ")

        result = sentiment_analysis(sentence)
        print(f"Sentiment: {result}")
        """,
        """A Idiot wrote this code""",
        """Execute the first""",
        """
        nltk.download('punkt')
        nltk.download('vader_lexicon')

        import nltk
        from nltk.sentiment.vader import SentimentIntensityAnalyzer
        
        def rule_based(sentence):
            analyzer = SentimentIntensityAnalyzer()
            scores = analyzer.polarity_scores(sentence)
            if scores['compound'] >= 0.05:
                return 'Positive'
            elif series['compound'] <= -0.05:
                return 'Negative'
            return 'Neutral'
        sentence = "This view is not bad"
        sentiment = rule_based(sentence)
        print(sentiment)
        """
    ]