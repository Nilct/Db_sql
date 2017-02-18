# Projet Normalisation / Dénormalisation

> Auteurs : Loïc Messal, Camille Parisel

## Sujet

> Réaliser une solution qui permet de visualiser la proximité de personnes physiques avec des entreprises proches en laissant à l’utilisateur le soin de préciser un rayon et une activité précise. Nous nous appuierons sur des fichiers en opendata de type Sirene, Bano et crawling/parsing.

## Analyse des données brutes

Le jeu de données est :

* Données [SIREN](http://www.data.gouv.fr/fr/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/), les données sont fournies sous forme de fichier csv listant toutes les entreprises en toute la France. En plus de ce fichier de 8.0Go, un fichier est publié tous les jours avec les modifications d'entreprises (création, fermeture, ...)
* Données [BANO](http://www.data.gouv.fr/fr/datasets/base-d-adresses-nationale-ouverte-bano/), c'est la Base d'Adresses Nationale Ouverte. Il est possible de ne télécharger que les département d'intêret.

Un premier travail de normalisation sur les adresses et les noms des entreprises est proposé dans le fichier **SIREN**. Il est malgré cela complexe à prendre en main :

* il est volumineux (8.0Go)
* il y a une centaine de champs dont certains sont redondants
* les adresses se trouvent dans les champs *déclarés*", *normalisés* et sous une 3ème forme. La différence réside dans la manière dont l'adresse est découpée et dans la "casse".

Les données **BANO** sont plus faciles à apréhender (moins de 10 champs) mais ne sont pas normalisées.

## Schéma Entité-Relation Initial

A partir des données dans les fichiers csv, on peut définir deux tables **SIREN** et **BANO** contenant les champs indispensables pour réaliser le projet.

> TODO schéma

L'objectif est de trouver l'enregistrement **BANO** (clé unique) qui correspond à chaque entreprise en manipulant les champs décrivant l'adresse présent dans chacune des tables.

A partir de ce schéma, et sans aucune optimisation, une requête pour répondre au projet, se déroule ainsi :

1. sélectionner tous les enregistrements de **BANO** dont la position est dans le périmètre autour de l'l’utilisateur
2. réaliser une jointure avec la table **SIREN** en manipulant les champs adresses des deux tables
3. retourner la liste des entreprises dont l'adresse se trouve dans le périmètre. 

## Optimisation avant mise en base de données

Notre objectif est de réaliser le projet pour le département 93 aussi :

* seules les données **BANO** du département 93 sont exploitées
* le fichier **SIREN** est filtré sur le département 93 (à l'aide d'un script `bash`), ce qui fait passer la taille du fichier de 8.0Go à 162Mo.

Une seconde optimisation a lieu via un script `python`, dont l'objectif est de *nettoyer* les données :
* les champs inutiles sont mis de côté
* les champs décrivant les adresses sont modifiés sur chacune des tables afin de faciliter l'appariement

Une troisième optimisation, qui peut se faire une fois en base à l'aide ou en amont est l'appariement des deux bases. Nous avons comparé l'efficacité de ces deux méthodes.



## Outils 

Le prétraitement des données est réalisé avec les languages / outils / bibliothèques suivants :

* **bash**, pour filter le département 93
* **python3**, avec :
  * **pandas** pour le chargement et la manipulation des données
  * **unidecode** pour la normalisation des champs d'adresses
  * **sqlalchemy** pour communiquer avec la base de Données

La base de données utilisée est **postgres**.

Pour la visualisation 

> TODO  

