# Base de données

## Création

A partir du [Tutoriel](https://suhas.org/sqlalchemy-tutorial).

Prérequis : postgres, pgAdmin

Création d'un utilisateur :
``` sh
$ sudo -i -u postgres
postgres@ubuntu:~$ psql
```

``` sql
postgres=# CREATE USER tp1;
CREATE ROLE
postgres=# ALTER ROLE tp1 WITH CREATEDB;
ALTER ROLE
postgres=# CREATE DATABASE bigdata1 OWNER tp1;
CREATE DATABASE
postgres=# ALTER USER tp1 WITH ENCRYPTED PASSWORD 'tp1';
ALTER ROLE
postgres=# \q
postgres@ubuntu:~$ psql bigdata1
psql (9.3.16)
Type "help" for help.

bigdata1=# GRANT ALL PRIVILEGES ON DATABASE bigdata1 TO tp1;
GRANT
bigdata1=# CREATE EXTENSION fuzzystrmatch;
CREATE EXTENSION
```


Ensuite lancer le script `python` :
``` sh
python3 dbmain.py setup_ubhome.json
```


## Manipulation de données

### Installation extension

CREATE EXTENSION fuzzystrmatch;

### Remplissage du champs BANO dans SIREN

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

Nombre de lignes non affectées :

> TODO



