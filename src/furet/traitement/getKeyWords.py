import argparse
import spacy
import os

from furet.traitement.getPdfText import *

nlp = spacy.load("fr_core_news_sm") # Loading french language of SpaCy's model

TITLES = {"m.", "mme.", "dr.", "prof.", "mlle.", "me."}

# Allows the lemmatize of keywords
def lemmatize_keywords(keywords):
    lemmatized = {}
    for kw in keywords:
        doc = nlp(kw.lower())
        lemmatized_kw = " ".join([token.lemma_ for token in doc])
        lemmatized[lemmatized_kw] = kw 
    return lemmatized

# If debug is then we display the (lemmatized) context of the keywords found, the number of occurrences, etc.
debug = False 

# Algo: For each keyword, we scan the text once, we lemmatize the text and keywords and look for keywords (lemmatized or not) that match the lemmatized text.

def getKeyWords(input_path, output_path, listeKeyWords):

    text = extract_text(input_path) # We retrieve the text
    doc = nlp(text.lower()) # We put everything in lower case

    # Lemmatization of text and keywords
    lemmatized_tokens = [token.lemma_ for token in doc if not token.is_punct and not token.is_space]
    lemmatized_kw = lemmatize_keywords(listeKeyWords)

    # (Debug) Useful for displaying contexts
    window_size = 3

    # Dictionary to store the number of occurrences of each keyword
    keyword_count = {}

    # (Debug) To annotate the text

    token_annotations = [""] * len(lemmatized_tokens)

    # Search for occurrences in the text for each keyword
    for kw_lemmatized in lemmatized_kw:

        original_kw = lemmatized_kw[kw_lemmatized]

        # If we have a word of several words, we divide it
        kw_lemmatized = kw_lemmatized.split()
        n = len(kw_lemmatized)

        original_kw_split = original_kw.split() 

        matches = []  # (Debug) Stores the positions of occurrences = Useful for displaying contexts

        # We look for occurrences of the keyword in the text (-n and i+n are used for keywords with several words)
        for i in range(len(lemmatized_tokens) - n + 1):
            if (lemmatized_tokens[i:i+n] == kw_lemmatized) or (lemmatized_tokens[i:i+n] == original_kw_split):
                if i > 0 and lemmatized_tokens[i - 1] in TITLES:
                    continue  # Ignore keyword matches in names
                matches.append(i)

        # Count and (Debug) show occurrences
        if matches:
            keyword_count[original_kw] = len(matches)  # Number of occurrences

            # (Debug)
            if(debug): 
                
                seen_contexts = set()
                # Show contexts (without repetition!!!!!!!!!!)
                for match in matches:
                    start = max(0, match - window_size)
                    end = min(len(lemmatized_tokens), match + n + window_size)
                    context = " ".join(lemmatized_tokens[start:end])
                    if context not in seen_contexts:
                        seen_contexts.add(context)
                        print(f"Contexte : ... {context} ...")
                
                # We annotate the text
                for match in matches:
                    for j in range(n):
                        pos = match + j
                        if token_annotations[pos] == "":
                            token_annotations[pos] = f"**{lemmatized_tokens[pos]}**({original_kw})"
    
                final_annotated = []
                for i, lemma in enumerate(lemmatized_tokens):
                    if token_annotations[i]:
                        final_annotated.append(token_annotations[i])
                    else:
                        final_annotated.append(lemma)

                annotated_text = " ".join(final_annotated)

                # We create a Markdown file for debugging with the annotated text
                name_fic_annoted = f"{output_path}_annoted.md"
                with open(name_fic_annoted , "w", encoding="utf-8") as f:
                    f.write(annotated_text)

                print(f"\nAnnotated text exported in : {name_fic_annoted}")

    return keyword_count
