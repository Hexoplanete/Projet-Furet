import argparse
import spacy
import os

from furet.traitement.getPdfText import *

nlp = spacy.load("fr_core_news_sm") # Chargement du modèle de langue français de SpaCy

TITLES = {"m.", "mme.", "dr.", "prof.", "mlle.", "me."}

KEYWORDS = [
    "chasse", "cynégétique", "gibier", "vénerie", "armes", "tir", "loup", "ours",
    "lynx", "chacal", "prédation", "prédateur", "tir de défense", "tir de prélèvement",
    "effarouchement", "blaireau", "déterrage", "louveterie", "louvetier", "piège", 
    "piégeage", "destruction", "battue", "ESOD", "espèce susceptible d'occasionner des dégâts",
    "sanglier", "lapin", "pigeon", "renard", "corvidés", "fouine", "martre", "belette", 
    "putois", "corbeau freux", "corneille noire", "pie bavarde", "geai", "étourneau"
]

# Permet de lemmatiser les mots clefs
def lemmatize_keywords(keywords):
    lemmatized = {}
    for kw in keywords:
        doc = nlp(kw.lower())
        lemmatized_kw = " ".join([token.lemma_ for token in doc])
        lemmatized[lemmatized_kw] = kw 
    return lemmatized

# # Arguments de ligne de commande
# parser = argparse.ArgumentParser()
# parser.add_argument("pdf_path", help="Chemin vers le fichier PDF à traiter")
# parser.add_argument(
#     "--debug", 
#     help="Si debug est alors on affiche le contexte (lemmatisé) des mots clefs trouvés, le nombre d'occurences, etc.", 
#     action="store_true"  # Cela fait de debug un booléen (True si argument est présent)
# )

# args = parser.parse_args()

# input_path_pdf = args.pdf_path
# debug = args.debug

debug = False

# Algo : Pour chaque mot clef, on va parcourir le texte 1 fois

def getKeyWords(input_path):

    text = extract_text(input_path) # On récupère le texte
    doc = nlp(text.lower()) # On met tout en lower case

    # Lemmatisation du texte et des mots clefs
    lemmatized_tokens = [token.lemma_ for token in doc if not token.is_punct and not token.is_space]
    lemmatized_kw = lemmatize_keywords(KEYWORDS)

    # (Debug) Utile pour l'affichage des contextes 
    window_size = 3

    # Dictionnaire pour stocker le nombre d'occurrences de chaque mot clef
    keyword_count = {}

    # (Debug) Pour annoter le texte
    token_annotations = [""] * len(lemmatized_tokens)

    # Recherche des occurrences dans le texte pour chaque mot-clé
    for kw_lemmatized in lemmatized_kw:

        original_kw = lemmatized_kw[kw_lemmatized]

        # Si on a un mot de plusieurs mots, on le divise
        kw_lemmatized = kw_lemmatized.split()
        n = len(kw_lemmatized)

        original_kw_split = original_kw.split() 

        matches = []  # (Debug) Stocke les positions des occurrences =  Utile pour l'affichage des contextes

        # On cherche les occurences du mot-clé dans le texte ( - n et i+n servent pour les mots clefs de plusieurs mots)
        for i in range(len(lemmatized_tokens) - n + 1):
            if (lemmatized_tokens[i:i+n] == kw_lemmatized) or (lemmatized_tokens[i:i+n] == original_kw_split):
                if i > 0 and lemmatized_tokens[i - 1] in TITLES:
                    continue  # Ignore les match de mot clef dans des noms
                matches.append(i)

        # Compter et (Debug) afficher les occurences
        if matches:
            keyword_count[original_kw] = len(matches)  # Nombre d'occurrences

            # (Debug)
            if(debug): 
                
                print(f"\n🔹 {original_kw} ({keyword_count[original_kw]} occurrence(s)) :")  # Afficher le mot-clé et le nombre d'occurrences
                seen_contexts = set()
                # Afficher les contextes (sans répétition !!!!!!!!!!)
                for match in matches:
                    start = max(0, match - window_size)
                    end = min(len(lemmatized_tokens), match + n + window_size)
                    context = " ".join(lemmatized_tokens[start:end])
                    if context not in seen_contexts:
                        seen_contexts.add(context)
                        print(f"Contexte : ... {context} ...")
                
                # On annote le texte
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

                # On crée un fichier Markdown pour debug avec le texte annoté
                name_fic_annoted = f"output/{os.path.basename(input_path)}_annoted.md"
                with open(name_fic_annoted , "w", encoding="utf-8") as f:
                    f.write(annotated_text)

                print(f"\nTexte annoté exporté dans : {name_fic_annoted}")

    return keyword_count
