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

Reading C:\Dev\CodePython\DB_sql\data\sirc-17804_9075_14209_201701_L_M_20170201_152507836_tor.csv
sys:1: DtypeWarning: Columns (13,15,16,24,29,36,41,49,53,61,62,63,65,68,75,76,78,82,90,91,92,93,94) have mixed types. Specify dtype option on import or set low_memory=False.

Data expected in C:\Dev\CodePython\DB_sql\data
Reading C:\Dev\CodePython\DB_sql\data\sirc-17804_9075_14209_201701_L_M_20170201_152507836_tor.csv
sys:1: DtypeWarning: Columns (13,15,16,24,29,36,41,49,53,61,62,63,65,68,75,76,78,82,90,91,92,93,94) have mixed types. Specify dtype option on import or set low_memory=False.
Keep following headers
['SIREN', 'NIC', 'L1_NORMALISEE', 'L2_NORMALISEE', 'L4_NORMALISEE', 'L5_NORMALISEE', 'L6_NORMALISEE', 'TYPVOIE', 'LIBVOIE', 'CODPOS', 'CEDEX', 'DEPET', 'APET700', 'LIBAPET', 'DAPET']
Rows before filtering by department : 10563603
Rows after filtering by department : 2863
Kept 2863 rows
Quick look
           SIREN  NIC                       NORM_ACRONYME  \
79      5720784  148             ETABLISSEMENTS DECAYEUX   
4895   16250102  155                 GROUPE CANDY HOOVER   
4998   16650111   95      MENUISERIE PACOTTE ET MIGNOTTE   
16956  38683728   18           SCI SAINT DENIS PRECHEURS   
17233  38688917   12  SYND COPR 47 R DES ARCHIVES 75003P   

                   NORM_NOM                NORM_ADRESSE NORM_BP  \
79                      NaN  1 IMPASSE NICEPHORE NIEPCE     NaN   
4895                    NaN                13 RUE AUGER     NaN   
4998                    NaN        28 AVENUE DE BOBIGNY     NaN   
16956    MME THERESE BOUDON            15 ALLEE WATTEAU     NaN   
17233  IS REP PAR SARL LOGI        2 BOULEVARD D AULNAY     NaN   

                        NORM_CP TYPVOIE           LIBVOIE   CODPOS    CEDEX  \
79     93290 TREMBLAY EN FRANCE     IMP  NICEPHORE NIEPCE  93290.0      NaN   
4895         93697 PANTIN CEDEX     RUE             AUGER  93500.0  93697.0   
4998         93130 NOISY LE SEC      AV        DE BOBIGNY  93130.0      NaN   
16956         93250 VILLEMOMBLE     ALL           WATTEAU  93250.0      NaN   
17233         93250 VILLEMOMBLE      BD          D AULNAY  93250.0      NaN   

      DEPET APET700                                           LIBAPET   DAPET  \
79       93   2599A       Fabrication d'articles métalliques ménagers  2011.0   
4895     93   4643Z      Commerce de gros d'appareils électroménagers  2008.0   
4998     93   4332A                 Travaux de menuiserie bois et PVC  2014.0   
16956    93   6820A                             Location de logements  2008.0   
17233    93   8110Z  Activités combinées de soutien lié aux bâtiments  2008.0   

       BANO_ID  
79          -1  
4895        -1  
4998        -1  
16956       -1  
17233       -1  

Process finished with exit code 0





