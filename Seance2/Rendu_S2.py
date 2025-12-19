import pandas as pd
import matplotlib.pyplot as plt


# Question 1
contenu = pd.read_csv(r"C:\Users\PC\Documents\Rendu\Seance2\src\data\resultats-elections-presidentielles-2022-1er-tour.csv")

# Question 2 
# Affichage du nombre de lignes et de colonnes
nb_lignes = len(contenu)
nb_colonnes = len(contenu.columns)
print(f"Nombre de lignes : {nb_lignes}, Nombre de colonnes : {nb_colonnes}")

# Question 3
# Affichage des types de données (int, float, object pour str)
# Les variables qualitatives apparaissent souvent comme 'object' et les quantitatives comme 'int64' ou 'float64'.
print(contenu.dtypes)

# Question 4
# Affichage des noms de colonnes via les premières lignes du tableau
print(contenu.head())

# Question 5
# Sélection de la colonne "Inscrits"
print(contenu["Inscrits"])

# Question 6
# Calcul des sommes des colonnes quantitatives (int ou float)
liste_sommes = []
for col in contenu.columns:
    if contenu[col].dtype == 'int64' or contenu[col].dtype == 'float64':
        liste_sommes.append(contenu[col].sum())
print(liste_sommes)

# Question 7
dossier_images = r"C:\Users\PC\Documents\Rendu\Seance2\src\data\Images"

# Nettoyage (conversion en nombres si nécessaire) et groupement des données
for col in ["Inscrits", "Votants"]:
    if contenu[col].dtype == 'object':
        contenu[col] = pd.to_numeric(contenu[col].astype(str).str.replace(" ", "").str.replace(",", "."), errors='coerce')

donnees_par_dept = contenu.groupby("Libellé du département")[["Inscrits", "Votants"]].sum()

for dept, row in donnees_par_dept.iterrows():
    plt.figure()
    plt.bar(["Inscrits", "Votants"], [row["Inscrits"], row["Votants"]])
    plt.title(f"Participation - {dept}")
    plt.savefig(f"{dossier_images}/{dept}.png")
    plt.close()

# Question 8
# L'objectif était de créer des diagrammes circulaires pour visualiser la répartition des votes (Blancs, Nuls, Exprimés, Abstentions) par département.
# Le code convertit les données en numérique et boucle sur les départements, mais il ne fonctionne pas actuellement.
dossier_pie = r"C:\Users\PC\Documents\Rendu\Seance2\src\data\Images_circulaire"

cols_pie = ["Blancs", "Nuls", "Exprimés", "Abstentions"]
for col in cols_pie:
    if contenu[col].dtype == 'object':
        contenu[col] = pd.to_numeric(contenu[col].astype(str).str.replace(" ", "").str.replace(",", "."), errors='coerce')

for dept, row in contenu.groupby("Libellé du département")[cols_pie].sum().iterrows():
    plt.figure()
    plt.pie(row, labels=cols_pie, autopct='%1.1f%%')
    plt.title(f"Répartition - {dept}")
    plt.savefig(f"{dossier_pie}/{dept}.png")
    plt.close()


# Question 9
# L'objectif était de tracer l'histogramme de la distribution des inscrits.
# L'option density=True sert à obtenir une distribution statistique (surface totale = 1). Le code est commenté car il ne fonctionne pas.
plt.figure()
plt.hist(contenu["Inscrits"], bins=50, density=True)
plt.title("Distribution des inscrits")
plt.savefig(f"{dossier_images}/histogramme_inscrits.png")
plt.close()
