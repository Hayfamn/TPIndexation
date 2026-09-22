import re
import math

STOPWORDS = {
    "le", "la", "les", "un", "une", "de", "des", "du",
    "et", "dans", "par", "pour", "d", "l", "est", "avec",
    "sur", "au", "aux", "en", "à", "ce", "qui"
}

def charger_documents(nom_fichier="documents.tsv"):
    documents = {}
    with open(nom_fichier, "r", encoding="utf-8") as fichier:
        for ligne in fichier:
            ligne = ligne.strip()
            if ligne:
                doc_id, contenu = ligne.split("\t", 1)
                documents[doc_id] = contenu
    return documents

def tokeniser(texte):
    return re.findall(r"\b\w+\b", texte.lower())

def preprocess(texte):
    return [t for t in tokeniser(texte) if t not in STOPWORDS]

def construire_index_inverse(documents):
    index_inverse = {}
    for doc_id, texte in documents.items():
        for terme in set(preprocess(texte)):
            index_inverse.setdefault(terme, []).append(doc_id)
    for terme in index_inverse:
        index_inverse[terme].sort()
    return index_inverse

def afficher_index(index_inverse):
    print("\n========== INDEX INVERSE ==========")
    for terme in sorted(index_inverse):
        print(f"{terme:15} -> {index_inverse[terme]}")

def intersection(list1, list2):
    i = j = 0
    resultat = []
    while i < len(list1) and j < len(list2):
        if list1[i] == list2[j]:
            resultat.append(list1[i])
            i += 1
            j += 1
        elif list1[i] < list2[j]:
            i += 1
        else:
            j += 1
    return resultat

def construire_sauts(postings):
    n = len(postings)
    if n < 2:
        return {}
    pas = max(1, int(math.sqrt(n)))
    sauts = {}
    position = 0
    while position + pas < n:
        sauts[position] = position + pas
        position += pas
    return sauts

def intersection_avec_sauts(list1, list2):
    i = j = 0
    resultat = []
    sauts1 = construire_sauts(list1)
    sauts2 = construire_sauts(list2)

    while i < len(list1) and j < len(list2):
        if list1[i] == list2[j]:
            resultat.append(list1[i])
            i += 1
            j += 1
        elif list1[i] < list2[j]:
            if i in sauts1 and list1[sauts1[i]] <= list2[j]:
                i = sauts1[i]
            else:
                i += 1
        else:
            if j in sauts2 and list2[sauts2[j]] <= list1[i]:
                j = sauts2[j]
            else:
                j += 1
    return resultat

def afficher_sauts(index_inverse):
    print("\n========== SKIP POINTERS ==========")
    for terme in sorted(index_inverse):
        sauts = construire_sauts(index_inverse[terme])
        if sauts:
            print(f"{terme:15} -> {sauts}")

def tests_intersection(index_inverse):
    tests = [
        ("maison", "jardin"),
        ("belle", "maison"),
        ("recherche", "documents"),
        ("chat", "jardin"),
        ("moteur", "documents")
    ]
    print("\n========== TESTS AND ==========")
    for terme1, terme2 in tests:
        docs1 = index_inverse.get(terme1, [])
        docs2 = index_inverse.get(terme2, [])
        print(f"{terme1} AND {terme2}")
        print("  Sans sauts :", intersection(docs1, docs2))
        print("  Avec sauts :", intersection_avec_sauts(docs1, docs2))

if __name__ == "__main__":
    documents = charger_documents()
    print("========== COLLECTION ==========")
    print("Nombre de documents :", len(documents))
    for doc_id, contenu in documents.items():
        print(f"{doc_id} : {contenu}")

    index_inverse = construire_index_inverse(documents)
    afficher_index(index_inverse)
    afficher_sauts(index_inverse)
    tests_intersection(index_inverse)

    print("\n========== TEST INTERACTIF ==========")
    terme1 = input("Entrez le premier terme : ").strip().lower()
    terme2 = input("Entrez le deuxième terme : ").strip().lower()
    docs1 = index_inverse.get(terme1, [])
    docs2 = index_inverse.get(terme2, [])
    print("Liste du premier terme :", docs1)
    print("Liste du deuxième terme :", docs2)
    print("Intersection sans skip pointers :", intersection(docs1, docs2))
    print("Intersection avec skip pointers :", intersection_avec_sauts(docs1, docs2))

