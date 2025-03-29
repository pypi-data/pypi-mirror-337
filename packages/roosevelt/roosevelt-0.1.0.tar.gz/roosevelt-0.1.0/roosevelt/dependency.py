def dependency():
    return [
        """
        import spacy
        from spacy import displacy
        """,
        """
        nlp = spacy.load("en_core_web_sm")
        """,
        """
        def dependency(sentence):
            doc = nlp(sentence)
            return doc
        """,
        """
        sentence = "The cat sat on the mat"
        """,
        """
        doc = dependency(sentence)
        """,
        """
        print(f"sentence: {sentence}")
        """,
        """
        for token in doc:
            print(f"{token.text:10} {token.dep_:10} {token.head.text:10}")
        """,
        """
        displacy.serve(doc, style="dep")
        """
    ]