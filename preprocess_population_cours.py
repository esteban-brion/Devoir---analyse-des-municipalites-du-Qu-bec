import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""
Ce script lit les donnees de statistiques canada 
de population des recensements 2021 et 2016
ainsi que la superficie des territoire recenses
et nettoye les donnees pour faciliter les analyses !
"""

# Base de donnees issue de Statistiques Canada
# Tableau 98-10-0002-02  Chiffres de population et des logements : Canada, provinces et territoires, et subdivisions de recensement (municipalités)"
# https://www150.statcan.gc.ca/t1/tbl1/fr/tv.action?pid=9810000202
# En français sans les symboles pour le QUEBEC
# Pour les besoin du cours : 
# - Index multilignes modifies 
# - en-tete et pied de page supprimes 

# delimiter ";" et non virgules car en francais
# decimal "," virgule en francais et non point
# thousands " " espace en francais et non virgule
# usecols pour ne conserver que les valeurs pertinentes

df = pd.read_csv('9810000202-sanssymbole-mod.csv',delimiter=';',decimal=',',thousands=' ',usecols=(0,1,2,3,11))

print('Avant traitement, liste des colonnes:\n')
print(df.columns)
print('\n')

# # On ne conserve que les donnees de populatione et la superficie
# # Supression des colonnes non pertinentes
# cols = list(df.columns)
# cols_to_drop = cols[4:11] + cols[12:]
# df.drop(axis=1,columns=cols_to_drop,inplace=True)

print('Apres drop des colonnes qui ne nous intetessent pas, liste des colonnes:\n')
print(df.columns)
print('\n')

# On renomme pour manipuler
df.columns = ['Nom','Type','Pop21','Pop16','Km2']


print('Avec les nouveaux noms, liste des colonnes:\n')
print(df.columns)
print('\n')

print(df.head())

print('dtype des differentes colonnes\n')
for col in df.columns:
    print(col,df[col].dtype)
print('\n')

print('Conversion des colonnes de population\n')

# Les espaces delimites les milliers, on les enleve
for col in ['Pop21','Pop16']:
    df[col] = df[col].apply(lambda x: x.replace(' ',''))

# Les ".."  correspondent a des valeurs non fournies, on les remplace par des NaN
df = df.replace('..', np.nan)

# On convertit finalement en float
for col in ['Pop21','Pop16']:
    df[col] = df[col].astype(float)

print('dtype des differentes colonnes\n')
for col in df.columns:
    print(col,df[col].dtype)
print('\n')

print("Youpi c'est des donnees numeriques!!\n")

print(df.head())
print('\n')

print(df.describe())
print('\n')

# On sauvegarde pour ne plus souffrir :D
df.to_csv('Census_2016_2021.csv')

# Créez une DataFrame pour les municipalités (type 'MÉ')
df_municipalites = df[df['Type'] == 'MÉ']

# Affichez le nombre de municipalités
nombre_municipalites = len(df_municipalites)
print("Nombre de municipalités :", nombre_municipalites)

# Calculez et affichez la population moyenne en 2016 et 2021
population_moyenne_2016 = df_municipalites['Pop16'].mean()
population_moyenne_2021 = df_municipalites['Pop21'].mean()

print("Population moyenne en 2016 :", population_moyenne_2016)
print("Population moyenne en 2021 :", population_moyenne_2021)

# Tracez un nuage de points du pourcentage d'accroissement de la population en fonction de la population en 2021
pourcentage_accroissement = ((df_municipalites['Pop21'] - df_municipalites['Pop16']) / df_municipalites['Pop16']) * 100
moyenne_pourcentage_accroissement = pourcentage_accroissement.mean()
print("moyenne pourcentege d'acroissement =", moyenne_pourcentage_accroissement)
plt.scatter(df_municipalites['Pop21'], pourcentage_accroissement)
plt.xlabel('Population en 2021')
plt.ylabel('Pourcentage d\'accroissement de la population (2016 à 2021)')
plt.title('Nuage de points : Accroissement de la population en fonction de la population en 2021')
plt.show()

# Classez les municipalités en 5 catégories selon leur population en 2021
bins = [0, 2000, 10000, 25000, 100000, np.inf]
labels = ['Moins de 2000 habitants', '2000 à 9999 habitants', '10000 à 24999 habitants', '25000 à 99999 habitants', '100000 et plus habitants']
df_municipalites.loc[:, 'Catégorie'] = pd.cut(df_municipalites['Pop21'], bins=bins, labels=labels, right=False)

# Tracez un diagramme en barres horizontales du nombre de municipalités dans chaque catégorie
plt.figure(figsize=(10, 6))
df_municipalites['Catégorie'].value_counts().sort_index().plot(kind='barh')
plt.xlabel('Nombre de municipalités')
plt.ylabel('Catégorie de population')
plt.title('Répartition des municipalités par catégorie de population en 2021')
plt.show()
