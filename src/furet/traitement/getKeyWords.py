import argparse
import spacy
import os

from furet.traitement.getPdfText import *

nlp = spacy.load("fr_core_news_sm") # Loading french language of SpaCy's model

TITLES = {"m.", "mme.", "dr.", "prof.", "mlle.", "me."}

# Allows the lemmatize of keywords
def lemmatizeKeywords(keywords):
    lemmatized = {}
    for kw in keywords:
        doc = nlp(kw.lower())
        lemmatized_kw = " ".join([token.lemma_ for token in doc])
        lemmatized[lemmatized_kw] = kw 
    return lemmatized

# If debug is then we display the (lemmatized) context of the keywords found, the number of occurrences, etc.
debug = False 


def getKeyWords(inputPath, outputPath, listeKeyWords):
    """
    Input : 
    
        inputPath  = Path of the PDF of the decree for which we want to find the matching keywords
        outputPath = Path to the annotated file used for debugging matched words
        listeKeyWords = The list of keywords provided by ASPAS

    Algorithm : 

        For each keyword, we scan the text once, we lemmatize the text and keywords and look for keywords 
        (lemmatized or not) that match the lemmatized text.
        

    """

    text = extractText(inputPath) # We retrieve the text
    doc = nlp(text.lower()) # We put everything in lower case

    # Lemmatization of text and keywords
    lemmatizedTokens = [token.lemma_ for token in doc if not token.is_punct and not token.is_space]
    lemmatized_kw = lemmatizeKeywords(listeKeyWords)

    # (Debug) Useful for displaying contexts
    windowSize = 3

    # Dictionary to store the number of occurrences of each keyword
    keywordCount = {}

    # (Debug) To annotate the text

    tokenAnnotations = [""] * len(lemmatizedTokens)

    # Search for occurrences in the text for each keyword
    for kw_lemmatized in lemmatized_kw:

        original_kw = lemmatized_kw[kw_lemmatized]

        # If we have a word of several words, we divide it
        kw_lemmatized = kw_lemmatized.split()
        n = len(kw_lemmatized)

        originalSplit_kw = original_kw.split() 

        matches = []  # (Debug) Stores the positions of occurrences = Useful for displaying contexts

        # We look for occurrences of the keyword in the text (-n and i+n are used for keywords with several words)
        for i in range(len(lemmatizedTokens) - n + 1):
            if (lemmatizedTokens[i:i+n] == kw_lemmatized) or (lemmatizedTokens[i:i+n] == originalSplit_kw):
                if i > 0 and lemmatizedTokens[i - 1] in TITLES:
                    continue  # Ignore keyword matches in names
                matches.append(i)

        # Count and (Debug) show occurrences
        if matches:
            keywordCount[original_kw] = len(matches)  # Number of occurrences

            # (Debug)
            if(debug): 
                
                seenContexts = set()
                # Show contexts (without repetition!!!!!!!!!!)
                for match in matches:
                    start = max(0, match - windowSize)
                    end = min(len(lemmatizedTokens), match + n + windowSize)
                    context = " ".join(lemmatizedTokens[start:end])
                    if context not in seenContexts:
                        seenContexts.add(context)
                        print(f"Contexte : ... {context} ...")
                
                # We annotate the text
                for match in matches:
                    for j in range(n):
                        pos = match + j
                        if tokenAnnotations[pos] == "":
                            tokenAnnotations[pos] = f"**{lemmatizedTokens[pos]}**({original_kw})"
    
                finalAnnotated = []
                for i, lemma in enumerate(lemmatizedTokens):
                    if tokenAnnotations[i]:
                        finalAnnotated.append(tokenAnnotations[i])
                    else:
                        finalAnnotated.append(lemma)

                annotatedText = " ".join(finalAnnotated)

                # We create a Markdown file for debugging with the annotated text
                nameFicAnnoted = f"{outputPath}_annoted.md"
                with open(nameFicAnnoted , "w", encoding="utf-8") as f:
                    f.write(annotatedText)

                print(f"\nAnnotated text exported in : {nameFicAnnoted}")

    return keywordCount
