# Projet Base de données SQL

## Données brutes

Le jeu de données est :

* Données **SIREN** : <http://www.data.gouv.fr/fr/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/>
* Données **BANO** : <http://www.data.gouv.fr/fr/datasets/base-d-adresses-nationale-ouverte-bano/>, contient les adresses (Base Adresses Nationale Ouverte), dataset [là](http://bano.openstreetmap.fr/data/)
> [Data.gouv.fr](http://www.data.gouv.fr/fr/datasets/base-d-adresses-nationale-ouverte-bano/) décrit le format des données

Au final, les fichiers suivants sont utilisés :

* sirene_201701_L_M.zip 1.5 Go, soit 8.0 Go une fois dézippé
* bano-93.csv 15.8 Mo (bano-93-shp.zip 8.4 Mo ?)

## Prétraitement 

### Bash 

On souhaite ne garder que les entreprises du 93 - Seine-Saint-Denis. Un premier filtre est appliqué pour ne garder que la première ligne d'entête et les lignes contenant '93' au champs du département.

``` sh
$ more sirc-17804_9075_14209_201701_L_M_20170201_152507836.csv | ./filter93.sh > sirc_201701_dep93.csv
```

Le fichier résultant fait 2.6 Go (à partir d'un fichier de 8.0 Go)

### Python

``` sh
$ python3 dbmain.py setup_ubuntu.json 
```

Le fichier json contient les chemins et les traitements à réaliser :

``` json
{
    "datapath": "/home/prof/work/Db_sql/data",
    "SIREN": "sirc-201701-with93.csv",
    "SIRENHeader": ["SIREN", "NIC", "L1_NORMALISEE", "L2_NORMALISEE", "L4_NORMALISEE", "L5_NORMALISEE", "L6_NORMALISEE", "TYPVOIE", "LIBVOIE", "CODPOS", "CEDEX", "DEPET", "APET700", "LIBAPET", "DAPET"],
    "SIRENHEADERRename": {
      "L1_NORMALISEE": "NORM_ACRONYME",
      "L2_NORMALISEE":"NORM_NOM",
      "L4_NORMALISEE":"NORM_ADRESSE",
      "L5_NORMALISEE": "NORM_BP",
      "L6_NORMALISEE": "NORM_CP"
    },
    "KEEP": {"DEPET":93},
    "BANO": "bano-93.csv",
      "BANOHeader": ["id", "numero", "voie", "code_post", "nom_comm", "source", "lat", "lon"],
      "update": false,
      "verbose": true
}
```
