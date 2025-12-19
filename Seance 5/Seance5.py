import pandas as pd
import math
import scipy
import scipy.stats

def ouvrirUnFichier(chemin):
    return pd.read_csv(chemin)

chemin = r"C:\Users\PC\Documents\Rendu\Seance 5\src\data\Echantillonnage-100-Echantillons.csv"
df = ouvrirUnFichier(chemin)

#Etape 1 Calcul des moyennes par colonne arrondies à l'entier avec round()
moyennes = df.mean().apply(lambda x: round(x))
print(moyennes)

#Etape 2 Calcul des fréquences (échantillon vs population mère)
somme_moyennes = moyennes.sum()
frequences_echantillon = (moyennes / somme_moyennes).round(2)
print(frequences_echantillon)

population_mere = pd.Series({'Pour': 852, 'Contre': 911, 'Sans opinion': 422})
frequences_population = (population_mere / population_mere.sum()).round(2)
print(frequences_population)

# Etape 3 : Calcul des intervalles de fluctuation et analyse
n = somme_moyennes # Taille de l'échantillon estimée
z_c = 1.96 # Seuil pour 95%

print("\n--- Analyse des intervalles de fluctuation (95%) ---")
for cat in frequences_population.index:
    p = frequences_population[cat]
    f_obs = frequences_echantillon[cat]
    
    # Calcul des bornes
    marge = z_c * math.sqrt((p * (1 - p)) / n)
    borne_inf = round(p - marge, 4)
    borne_sup = round(p + marge, 4)
    
    print(f"Catégorie '{cat}': Intervalle [{borne_inf}; {borne_sup}] - Observé: {f_obs}")
    if borne_inf <= f_obs <= borne_sup:
        print(f"  -> La fréquence observée est dans l'intervalle de fluctuation.")
    else:
        print(f"  -> La fréquence observée est HORS de l'intervalle.")

print("\n--- Conclusion du rapport ---")
print("L'intervalle de fluctuation est centré sur la valeur réelle de la population mère.")
print("Il représente la zone où 95% des fréquences d'échantillons devraient tomber par pur hasard.")
print("Si nos échantillons observés sont dans cet intervalle, ils sont représentatifs de la population mère.")

# Etape 4 : Intervalle de confiance (Estimation)
print("\n--- Etape 4 : Intervalle de confiance (Estimation) ---")

# Sélection du premier échantillon (iloc[0]) et conversion en liste
echantillon_1 = list(df.iloc[0])

# Calcul de la somme et des fréquences pour cet échantillon
n_local = sum(echantillon_1)
freqs_local = [x / n_local for x in echantillon_1]

# Calcul de l'intervalle de confiance (formule simplifiée 1/sqrt(n))
marge_confiance = 1 / math.sqrt(n_local)

for i, col in enumerate(df.columns):
    f = freqs_local[i]
    b_inf = round(f - marge_confiance, 4)
    b_sup = round(f + marge_confiance, 4)
    print(f"Catégorie '{col}': Fréquence {round(f, 4)} -> IC [{b_inf}; {b_sup}]")
    
    if col in frequences_population:
        p_reelle = frequences_population[col]
        status = "CONTIENT" if b_inf <= p_reelle <= b_sup else "NE CONTIENT PAS"
        print(f"  -> L'intervalle {status} la valeur réelle ({p_reelle}).")

print("\n--- Interprétation ---")
print("L'intervalle de confiance part de l'échantillon pour estimer la population mère (démarche inverse de la fluctuation).")
print("Avec la formule simplifiée 1/sqrt(n), on obtient une fourchette qui a 95% de chances de contenir la vraie valeur.")

# Etape 5 : Test de Shapiro-Wilk pour la normalité
print("\n--- Etape 5 : Test de Shapiro-Wilk ---")

chemin_test1 = r"C:\Users\PC\Documents\Rendu\Seance 5\src\data\Loi-normale-Test-1.csv"
chemin_test2 = r"C:\Users\PC\Documents\Rendu\Seance 5\src\data\Loi-normale-Test-2.csv"

# On récupère la première colonne de chaque fichier
data1 = ouvrirUnFichier(chemin_test1).iloc[:, 0]
data2 = ouvrirUnFichier(chemin_test2).iloc[:, 0]

stat1, p_value1 = scipy.stats.shapiro(data1)
stat2, p_value2 = scipy.stats.shapiro(data2)

print(f"Fichier 1 : p-value = {p_value1:.6f}")
print(f"Fichier 2 : p-value = {p_value2:.6f}")

print("\n--- Rapport ---")
print("Le test de Shapiro-Wilk pose l'hypothèse nulle (H0) que la distribution est normale.")
print(f"Fichier 1 : {'Distribution NORMALE (On ne rejette pas H0 car p > 0.05)' if p_value1 > 0.05 else 'Distribution NON normale (On rejette H0 car p < 0.05)'}")
print(f"Fichier 2 : {'Distribution NORMALE (On ne rejette pas H0 car p > 0.05)' if p_value2 > 0.05 else 'Distribution NON normale (On rejette H0 car p < 0.05)'}")
