import pandas as pd
import numpy as np
from scipy.stats import spearmanr, kendalltau

# Charger le fichier CSV
df = pd.read_csv(r"C:\Users\PC\Documents\Seance6\src\data\Le-Monde-HS-Etats-du-monde-2007-2025.csv")

# Sélection des colonnes
colonnes = ["État", "Pop 2007", "Pop 2025", "Densité 2007", "Densité 2025"]
df_selection = df[colonnes]
print(df_selection.head())

def ordreDecroissant(liste):
    return sorted(liste, key=lambda x: x[0], reverse=True)

def ordrePopulation(pop, etat):
    ordrepop = []
    for i in range(len(pop)):
        try:
            val = float(pop[i])
        except Exception:
            continue
        if not np.isnan(val):
            ordrepop.append([val, etat[i]])
    ordrepop = ordreDecroissant(ordrepop)
    for idx in range(len(ordrepop)):
        ordrepop[idx] = [idx + 1, ordrepop[idx][1]]
    return ordrepop

# Préparer listes de base
etat = df_selection["État"].tolist()
pop_2007 = df_selection["Pop 2007"].tolist()
pop_2025 = df_selection["Pop 2025"].tolist()
dens_2007 = df_selection["Densité 2007"].tolist()
dens_2025 = df_selection["Densité 2025"].tolist()

ordre_pop_2007 = ordrePopulation(pop_2007, etat)
ordre_pop_2025 = ordrePopulation(pop_2025, etat)
ordre_dens_2007 = ordrePopulation(dens_2007, etat)
ordre_dens_2025 = ordrePopulation(dens_2025, etat)

print("Ordre décroissant Pop 2007 :", ordre_pop_2007)
print("Ordre décroissant Pop 2025 :", ordre_pop_2025)
print("Ordre décroissant Densité 2007 :", ordre_dens_2007)
print("Ordre décroissant Densité 2025 :", ordre_dens_2025)

def classementPays(ordre1, ordre2):
    # ordre1 et ordre2 : [[rang, pays], ...]
    rank1 = {pays: rang for rang, pays in ordre1}
    rank2 = {pays: rang for rang, pays in ordre2}
    classement = []
    # itérer pays par ordre croissant du rang dans ordre1 (classement 2007)
    for pays, rang_pop in sorted(rank1.items(), key=lambda x: x[1]):
        if pays in rank2:
            classement.append([rang_pop, rank2[pays], pays])
    return classement

# Comparaison des classements population/densité pour 2007 et 2025
comparaison_2007 = classementPays(ordre_pop_2007, ordre_dens_2007)
comparaison_2025 = classementPays(ordre_pop_2025, ordre_dens_2025)

print("Comparaison Population/Densité 2007 :")
print(comparaison_2007)

print("Comparaison Population/Densité 2025 :")
print(comparaison_2025)

# Extraire listes de rangs pour calculs de corrélation
rangs_pop_2007 = [p for p, d, _ in comparaison_2007]
rangs_dens_2007 = [d for p, d, _ in comparaison_2007]
rangs_pop_2025 = [p for p, d, _ in comparaison_2025]
rangs_dens_2025 = [d for p, d, _ in comparaison_2025]

# Calcul des coefficients de corrélation des rangs
spearman_2007, _ = spearmanr(rangs_pop_2007, rangs_dens_2007)
kendall_2007, _ = kendalltau(rangs_pop_2007, rangs_dens_2007)

spearman_2025, _ = spearmanr(rangs_pop_2025, rangs_dens_2025)
kendall_2025, _ = kendalltau(rangs_pop_2025, rangs_dens_2025)

print("Spearman 2007 :", spearman_2007)
print("Kendall 2007  :", kendall_2007)
print("Spearman 2025 :", spearman_2025)
print("Kendall 2025  :", kendall_2025)