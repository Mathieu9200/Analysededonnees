import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

contenu = pd.read_csv(r"C:\Users\PC\Documents\Rendu\Seance 3\src\data\resultats-elections-presidentielles-2022-1er-tour.csv")
island_data = pd.read_csv(r"C:\Users\PC\Documents\Rendu\Seance 3\src\data\island-index.csv", sep=',')

# Etape 1 
# Sélectionner les colonnes contenant des caractères quantitatifs
df_quant = contenu.select_dtypes(include=[np.number])

# Calculer les statistiques demandées (arrondies à 2 décimales)

# Moyennes
moyennes = df_quant.mean().round(2)

# Médianes
medianes = df_quant.median().round(2)

# Modes (on prend la première ligne si multimodal)
modes = df_quant.mode().iloc[0].round(2)

# Écart type
ecart_type = df_quant.std().round(2)

# Écart absolu à la moyenne (utilisation de np.abs())
ecart_absolu_moyen = np.abs(df_quant - df_quant.mean()).mean().round(2)

# Étendue (utilisation de min() et max() de Pandas)
etendue = (df_quant.max() - df_quant.min()).round(2)

# Etape 2 Afficher la liste des paramètres sur le terminal
print("Moyennes :\n", moyennes)
print("Médianes :\n", medianes)
print("Modes :\n", modes)
print("Écart type :\n", ecart_type)
print("Écart absolu moyen :\n", ecart_absolu_moyen)
print("Étendue :\n", etendue)

# Etape 3 Calculer la distance interquartile et interdécile
iqr = (df_quant.quantile(0.75) - df_quant.quantile(0.25)).round(2)
idr = (df_quant.quantile(0.9) - df_quant.quantile(0.1)).round(2)

print("Distance interquartile (IQR) :\n", iqr)
print("Distance interdécile (IDR) :\n", idr)

# Etape 4 Génération des boîtes à moustache pour chaque colonne quantitative
output_dir = r"C:\Users\PC\Documents\Rendu\Seance 3\src\IMG"

for col in df_quant.columns:
    plt.figure()
    plt.boxplot(df_quant[col].dropna())
    plt.title(f"Boîte à moustache : {col}")
    plt.savefig(f"{output_dir}\\boxplot_{col}.png")
    plt.close()

# Etape 5 : Catégorisation et dénombrement des îles selon la surface
# Définition des bornes pour les intervalles demandés
bins = [0, 10, 25, 50, 100, 2500, 5000, 10000, np.inf]
# Définition des étiquettes pour chaque intervalle
labels = [']0,10]', ']10,25]', ']25,50]', ']50,100]', ']100,2500]', ']2500,5000]', ']5000,10000]', ']10000,+inf[']

# Utilisation de pd.cut pour catégoriser la colonne 8 (index 7)
island_data['Categorie_Surface'] = pd.cut(island_data.iloc[:, 7], bins=bins, labels=labels)

# Dénombrement des îles par catégorie
repartition_surface = island_data['Categorie_Surface'].value_counts().sort_index()
print("Répartition des îles par surface :\n", repartition_surface)
