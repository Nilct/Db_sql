Détermination de l'adresse du premier résultat :

SELECT * FROM "SIREN" LIMIT 1;



##  Recherche du 8 rue isaac newton dans le 93150

Réduction au code postal
```sql
SELECT * FROM "BANO" WHERE "code_post"=93150 ORDER BY "voie";
```


Levenshtein sur le libellé de la voirie
```sql
SELECT * FROM "BANO" WHERE "code_post"=(SELECT "codpos" FROM "SIREN" WHERE "siren"=316475722) ORDER BY levenshtein((SELECT "libvoie" FROM "SIREN" WHERE "siren"=316475722), voie);
```
    => Problème du fait de la non atomicité des libellés


Levenshtein avec concaténation du type de voie et du libellé de la voirie :
```sql
SELECT * FROM "BANO" WHERE "code_post"=(SELECT "codpos" FROM "SIREN" WHERE "siren"=316475722) ORDER BY levenshtein((SELECT "typvoie"||"libvoie" FROM "SIREN" WHERE "siren"=316475722), voie);
```
    => La rue isaac newton apparaît mais ce n'est pas le premier résultat...



Utilisation du match entre les numéros (a nécessité de caster les types text en INT (les numéros de type 26BIS ont donc été initialisés à NaN... )) :
```sql
SELECT * FROM "BANO" WHERE "code_post"=(SELECT "codpos" FROM "SIREN" WHERE "siren"=316475722) AND CAST("numero" AS INTEGER)=(CAST((SELECT "numvoie" FROM "SIREN" WHERE "siren"=316475722) AS INTEGER)) ORDER BY levenshtein((SELECT "typvoie"||"libvoie" FROM "SIREN" WHERE "siren"=316475722), voie);
```
    Le premier résultat correspond bien au 8 rue isaac newton dans le 93150. La requête est satisfaisante !
