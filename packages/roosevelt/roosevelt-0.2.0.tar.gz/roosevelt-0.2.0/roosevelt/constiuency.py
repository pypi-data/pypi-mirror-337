def constiuency():
    return [
        """
        import stanza
        import nltk
        from nltk.tree import Tree
        """,
        """
        nlp = stanza.Pipeline('en')
        """,
        """
        # Example sentence
        sentence = "The cat sat on the mat."

        # Process the sentence using the stanza pipeline
        doc = nlp(sentence)
        """,
        """
        # Get the constituency tree
        for sentence in doc.sentences:
            constituency_tree = sentence.constituency

            # Convert the string representation to a Tree object
            tree = Tree.fromstring(str(constituency_tree))

            # Display the tree
            tree.pretty_print()
        """
    ]