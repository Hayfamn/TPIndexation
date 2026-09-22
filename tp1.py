import re
import time

STOPWORDS = {
    "le", "la", "les", "un", "une",
    "de", "des", "du", "et", "dans",
    "par", "pour", "d", "l"
}


# =========================
# Exercice 1 : chargement
# =========================
def charger_documents(nom_fichier="documents.tsv"):
    documents = {}

    with open(nom_fichier, "r", encoding="utf-8") as fichier:
        for ligne in fichier:
            ligne = ligne.strip()
            if not ligne:
                continue

            doc_id, contenu = ligne.split("\t", 1)
            documents[doc_id] = contenu

    return documents


# =========================
# Exercice 2 : recherche naïve
# =========================
def recherche_naive(terme, documents):
    resultats = []

    for doc_id, texte in documents.items():
        if terme.lower() in texte.lower():
            resultats.append(doc_id)

    return resultats


# =========================
# Exercice 3 : prétraitement
# =========================
def tokeniser(texte):
    return re.findall(r"\b\w+\b", texte.lower())


def supprimer_stopwords(tokens):
    return [token for token in tokens if token not in STOPWORDS]


# =========================
# Exercice 4 : prétraitement complet
# =========================
def preprocess(texte):
    tokens = tokeniser(texte)
    tokens = supprimer_stopwords(tokens)
    return tokens


# =========================
# Exercice 5 : index inversé
# =========================
def construire_index(documents):
    index_inverse = {}

    for doc_id, texte in documents.items():
        termes = preprocess(texte)

        for terme in set(termes):
            if terme not in index_inverse:
                index_inverse[terme] = []

            index_inverse[terme].append(doc_id)

    # Les postings doivent être triés pour l'intersection.
    for terme in index_inverse:
        index_inverse[terme].sort()

    return index_inverse


def afficher_index(index_inverse):
    print("\n===== INDEX INVERSE =====")
    for terme in sorted(index_inverse):
        print(f"{terme} -> {index_inverse[terme]}")


# =========================
# Exercice 6 : recherche indexée
# =========================
def rechercher(terme, index_inverse):
    return index_inverse.get(terme.lower(), [])


# =========================
# Exercice 7 : intersection
# =========================
def intersection(list1, list2):
    i = 0
    j = 0
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


# =========================
# Exercice 8 : comparaison
# =========================
def mesurer_recherche(terme, documents, index_inverse):
    debut = time.perf_counter()
    resultat_naif = recherche_naive(terme, documents)
    temps_naif = time.perf_counter() - debut

    debut = time.perf_counter()
    resultat_index = rechercher(terme, index_inverse)
    temps_index = time.perf_counter() - debut

    return resultat_naif, resultat_index, temps_naif, temps_index


def generer_collection(nombre):
    collection = {}

    phrases = [
        "La recherche permet de retrouver des documents pertinents",
        "Un moteur de recherche utilise un index inversé",
        "L indexation facilite la recherche rapide des informations",
        "Les documents sont classes selon leur pertinence",
        "La recherche web traite une grande collection de documents"
    ]

    for i in range(1, nombre + 1):
        collection[f"D{i}"] = phrases[i % len(phrases)]

    return collection


def comparaison_temps():
    print("\n===== COMPARAISON EXPERIMENTALE =====")
    print(f"{'Documents':<12}{'Naïve (s)':<18}{'Indexée (s)':<18}")

    for taille in [100, 1000, 10000]:
        collection = generer_collection(taille)
        index = construire_index(collection)

        debut = time.perf_counter()
        recherche_naive("recherche", collection)
        temps_naif = time.perf_counter() - debut

        debut = time.perf_counter()
        rechercher("recherche", index)
        temps_index = time.perf_counter() - debut

        print(f"{taille:<12}{temps_naif:<18.8f}{temps_index:<18.8f}")


# =========================
# Programme principal
# =========================
if __name__ == "__main__":
    documents = charger_documents()

    print("===== COLLECTION =====")
    print("Nombre de documents :", len(documents))

    for doc_id, contenu in documents.items():
        print(f"{doc_id} : {contenu}")

    print("\n===== PRETRAITEMENT =====")
    for doc_id, contenu in documents.items():
        print(f"{doc_id} -> {preprocess(contenu)}")

    index_inverse = construire_index(documents)
    afficher_index(index_inverse)

    # 5 tests de recherche à un terme
    print("\n===== 5 TESTS DE RECHERCHE =====")
    tests = ["recherche", "moteur", "index", "documents", "blockchain"]

    for terme in tests:
        naive = recherche_naive(terme, documents)
        indexee = rechercher(terme, index_inverse)
        print(f"{terme} -> naïve: {naive} | indexée: {indexee}")

    # 3 tests AND
    print("\n===== 3 TESTS AND =====")
    tests_and = [
        ("recherche", "documents"),
        ("moteur", "recherche"),
        ("index", "recherche")
    ]

    for terme1, terme2 in tests_and:
        docs1 = rechercher(terme1, index_inverse)
        docs2 = rechercher(terme2, index_inverse)
        resultat = intersection(docs1, docs2)

        print(
            f"{terme1} AND {terme2} -> "
            f"{resultat}"
        )

    # Comparaison
    print("\n===== COMPARAISON NAÏVE / INDEXÉE =====")
    resultat_naif, resultat_index, temps_naif, temps_index = mesurer_recherche(
        "recherche", documents, index_inverse
    )

    print("Résultat naïf :", resultat_naif)
    print("Résultat indexé :", resultat_index)
    print(f"Temps naïf : {temps_naif:.8f} s")
    print(f"Temps indexé : {temps_index:.8f} s")

    comparaison_temps()
