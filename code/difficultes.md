# Difficultées rencontrées :

### BANO (à vérifier):
La base d'adresse nationale ouverte est indiquée comme étant encodée en utf-8 (voir [bano.png](image)).
Or le csv téléchargé est encodé en latin-1.


### DBdesigner :
Lorsqu'on configure un nouveau projet adapté pour les bases de données postgrés, Il autorise le type 'double' pour les attributs. Il conserve le type 'double' lors de l'export sql. Cependant, postgrès utilise le type 'double precision' et non le type 'double'.  


### Nomenclature des adresses différentes
Pour contrer cela, nous avons utilisé la distance de Levenshtein (qui se base sur les chaînes de Markov) afin de retrouver l'adresse dans la base de données qui se rapproche le plus de celle demandée par l'utilisateur). Dans psql, la fonction de Levenshtein est implémentée dans le module fuzzystrmatch. Il faut d'abord activer l'extension avant de pouvoir l'utiliser.

```sql
CREATE EXTENSION fuzzystrmatch;
```

Exemple de requête pour les matchs d'adresses :

```sql
SELECT * FROM "BANO" ORDER BY levenshtein('Rue de l abeill', voie);
```
