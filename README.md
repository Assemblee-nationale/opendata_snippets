# opendata_snippets
Quelques exemples et outils pour exploiter les données mise à disposition sur le site data.assemblee-nationale.fr

# Introduction

Les flux Opendata de l'Assemblée nationale ont été conçus avec les buts suivants :
  * Compléter  le site de l'Assemblée qui est la première source de données pour le citoyen intéressé par un point spécifique ou un texte de loi particulier.
  * Faciliter une exploitation informatique des données
  * Exposer autant que possible la richesse des données disponibles sans procéder à des choix arbitraires parmi celles-ci
  * Utiliser des formats pérennes et neutres non liès à des fournisseurs particuliers.

## Comprendre les "fluxs" ou fichiers

Les fichiers sont primairement des fichiers XML (le format JSON et le CSV sont dérivé du XML),
conçus pour permettre le chargement d'une base de donnée, d'un datacube ou d'une base NoSQL de votre choix
en une seule "passe", c'est à dire en lisant le fichier une seule fois.

C'est pourquoi par exemple les flux 'acteurs mandats organes' comprennent la liste des organes puis
les acteurs avec leurs mandats insérés (car les "mandats"  d'un acteur référencent des organes).

Cette organisation peut cependant rendre ces fluxs "trop riches" et "gros" pour certains usages...

## Buts de ce "repos" git

Le but de ce repos git est de fournir des exemples de reformatage, exploitation ou restructuration de ces jeux de données
pour les rendre moins "intimidants" et générer des idées d'usage.

A terme le souhait est d'enrichir ces exemples avec vos contributions.

# Les "snippets"

## split-datas.py

Ce fragment de code montre comment diviser le flux en autant de petits fichiers représentant chacun un concept du référentiel (organe, acteur, compte rendu Syceron, etc ..)
 
* il introduit une fonction utilitaire "fragparse" permettant de parcourir un jeu de données et d'en extraire les informations voulues (SAX parser)
* il montre comment parcourir un fichier XML volumineux sans le charger entièrement en mémoire quand seule une partie des données vous intéresse.

 

## restructure.py

Ce fragment de code construit un fichier "CSV" à partir d'un jeux de donnée en restructurant les données du flux.
En l'occurence le code produit un fichier CSV dans lequel chaque ligne contient un acteur et la liste de ses mandats avec le nom de l'organe sur lequel porte le mandat.
Comme ceci :
```(['[PA267328] M. Cédric Perrin-1974/01/20'], 'PM703547-Sénat ( 5ème République )-2014/10/01--SENAT;PM704067-Commission des affaires étrangères, de la défense et des forces armées-2014/10/08--COMSENAT;PM704332-Groupe Les Républicains-2014/10/07--GROUPESENAT')```

Ce fragment se base sur le parcours des données XML en mémoire au moyen d'une interface de type "DOM parser"

## Installer / tester le code
