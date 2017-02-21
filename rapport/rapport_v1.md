# Projet Normalisation / Dénormalisation

> Auteurs : Loïc Messal, Camille Parisel

## Sujet

> Réaliser une solution qui permet de visualiser la proximité de personnes physiques avec des entreprises proches en laissant à l’utilisateur le soin de préciser un rayon et une activité précise. Nous nous appuierons sur des fichiers en opendata de type Sirene, Bano et crawling/parsing.

L'objectif est de se rendre compte de la difficulté des traitements nécessaires pour exploiter de *relativement* gros volumes de données et des possibilités d'optimisation :

* phase de préparation des données préalablement à la mise en base 
	* (*pas fait ici*) des outils permettent de réaliser les traitements de manière distribuée (ici on a privilégié des outils et langage déjà connus)
* optimisation des tables 
	* choix des types pour champs (et longueur de champs pour VARCHAR())
	* mise en place de la géolocation
	* indexation pour accélérer les requêtes 

## Analyse des données brutes

Le jeu de données est :

* Données [SIREN](http://www.data.gouv.fr/fr/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/), les données sont fournies sous forme de fichier csv listant toutes les entreprises en toute la France. En plus de ce fichier de 8.0Go, un fichier est publié tous les jours avec les modifications d'entreprises (création, fermeture, ...)
* Données [BANO](http://www.data.gouv.fr/fr/datasets/base-d-adresses-nationale-ouverte-bano/), c'est la Base d'Adresses Nationale Ouverte. Il est possible de ne télécharger que les département d'intêret.

Un premier travail de normalisation sur les adresses et les noms des entreprises est proposé dans le fichier **SIREN**. Il est malgré cela complexe à prendre en main :

* il est volumineux (8.0Go)
* il y a une centaine de champs dont certains sont redondants
* les adresses se trouvent dans les champs *déclarés*, *normalisés* et sous une 3ème forme. La différence réside dans la manière dont l'adresse est découpée et dans la "casse".

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

Une troisième optimisation, qui peut se faire une fois en base à l'aide ou en amont est l'appariement des deux bases. 

### Manipulations sous python

Une fois les fichiers chargés, les champs inutiles sont éliminés. Ensuite chaque tables (*dataframes* sous python), sont enrichies de nouvelle colonnes préparant la future requête de géolocation.

### Requête sous postgres

Les bases importées sous postgres sont :
``` sql
CREATE TABLE public.bano
(
  index bigint,
  id text,
  numero text,
  voie text,
  code_post bigint,
  nom_comm text,
  source text,
  lat double precision,
  lon double precision,
  "ADD_num_voie" text,
  "ADD_ind_rep" text,
  "ADD_caps_voie" text,
  "ADD_caps_nom_comm" text
)
WITH (
  OIDS=FALSE
);
```
et

``` sql
CREATE TABLE public.siren
(
  index bigint,
  "SIREN" bigint,
  "NIC" bigint,
  "NORM_ACRONYME" text,
  "NORM_NOM" text,
  "NORM_ADRESSE" text,
  "NORM_BP" text,
  "NORM_CP" text,
  "NUMVOIE" text,
  "INDREP" text,
  "TYPVOIE" text,
  "LIBVOIE" text,
  "CODPOS" bigint,
  "CEDEX" double precision,
  "DEPET" bigint,
  "LIBCOM" text,
  "APET700" text,
  "LIBAPET" text,
  "DAPET" bigint,
  "ADD_VOIE" text,
  "ADD_LIBCOM" text,
  "BANO_ID" text
)
WITH (
  OIDS=FALSE
);
```

La requête pour associer les entreprises à la bonne adresse est :
``` sql
UPDATE siren s
SET "BANO_ID" = (SELECT b.id
	FROM bano b
	WHERE b.code_post = s."CODPOS"
	AND b."ADD_caps_nom_comm" = s."ADD_LIBCOM"
	AND b."ADD_num_voie" = s."NUMVOIE" 
    AND levenshtein_less_equal(b."ADD_caps_voie", s."ADD_VOIE", 5)<6
    ORDER BY levenshtein_less_equal(b."ADD_caps_voie", s."ADD_VOIE", 5) 
    LIMIT 1
    )
```

![EXPLAIN de la requête](./Explain_SIRENBANO.png  "EXPLAIN")

### Métriques 

* chargement et nettoyage du BANO (python)
* chargement et nettoyage du SIREN (python)
* insertion dans postgres (python) 
* geolocation (requête sql)

``` sh
nil@Arthur:~/Dev/Db_sql/code$ python3 dbmain.py setup_ubhome.json
Data expected in /home/nil/Dev/Db_sql/data
Reading /home/nil/Dev/Db_sql/data/bano-93.csv
Kept 203507 rows
Total time taken: 2 second(s)
Reading /home/nil/Dev/Db_sql/data/sirc_201701_dep93.csv
sys:1: DtypeWarning: Columns (16,65,68,82,90,91,92,93,94) have mixed types. Specify dtype option o
n import or set low_memory=False.
Kept 206032 rows
Total time taken: 4 second(s)
Engine(postgresql://tp1:***@localhost:5432/bigdata1)
MetaData(bind=Engine(postgresql://tp1:***@localhost:5432/bigdata1))
Total time taken: 49 second(s)

```

Sous postgres :

``` sql
Query returned successfully: 206032 rows affected, 01:03:3601 hours execution time.
```

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

