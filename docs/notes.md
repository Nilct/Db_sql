# Notes TP1 Postgre / Postgis

## Sujet

A partir d'une position dans le 93-Seine-Saint-Denis, d'un rayon et d'un type d'activité, donner les entreprises à proximité avec leur distance à la position.

* **Input** : lat/long (deg, WGS84), rayon (m), activité (énumération)
* **Output** : Liste des entreprise (Nom, lat/long, distance, activité, adresse)

### Etapes

* Définir les tables et les champs
* Remplir les tables à partir des données SIREN et BANO (et OSM ?)
* Ecrire la requête calculant la distance (procédure ??)
* Visualisation
* GUI pour la requête

## Logiciels

* **postgre** `sudo apt-get install -V postgresql` pour la version 9.5
(vérifier sudo apt-get install postgresql libpq-dev postgresql-client postgresql-client-common)

* *postgis* `sudo apt-get install -V postgis` **à ne pas utiliser**
* **pgadmin** `sudo apt-get install -V pgadmin3`
* *qgis*

### Python

Vérifier l'intérêt d'utiliser psycopg2

<https://www.fullstackpython.com/blog/postgresql-python-3-psycopg2-ubuntu-1604.html>
> donne info sur démarrage postgre, création user

Pb de coordonnées 
http://altons.github.io/python/2012/12/01/converting-northing-and-easting-to-latitude-and-longitude/
Then I came across a python package called Pyproj which along with Pandas solved my problem easily (well, after couple of days of research).

Anaconda cheat sheet
<http://altons.github.io/python/2014/04/12/conda-commands/>

### MongoDB

Aide mémoire (pas récent!)
http://altons.github.io/python/2013/01/21/gentle-introduction-to-mongodb-using-pymongo/

## Jeu de données

* Données **SIREN** : <http://www.data.gouv.fr/fr/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/>
* Données **OSM** : <http://download.geofabrik.de/europe/france/ile-de-france.html>, format *osm.pbf* et *shp.zip*
* Données **BANO** : <http://www.data.gouv.fr/fr/datasets/base-d-adresses-nationale-ouverte-bano/>, contient les adresses (Base Adresses Nationale Ouverte), dataset [là](http://bano.openstreetmap.fr/data/)
> [Data.gouv.fr](http://www.data.gouv.fr/fr/datasets/base-d-adresses-nationale-ouverte-bano/) décrit le format des données

Au final, les fichiers suivants sont utilisés :

* sirene_201701_L_M.zip 1.5 Go
* bano-93.csv 15.8 Mo (bano-93-shp.zip 8.4 Mo ?)
* ile-de-france-latest.osm.pbf 233 Mo

### BANO Format de diffusion

Ces fichiers sont proposés sous forme de :

* fichiers csv (projection WGS84/EPSG:4326 et textes en UTF-8)
* fichiers shapefile (EPSG:4326 et UTF-8)
* données RDF au format turtle

## Description des tables

### Entreprises / SIREN

<https://www.insee.fr/fr/information/2406147> nomenclature activité fr (NAF) 






