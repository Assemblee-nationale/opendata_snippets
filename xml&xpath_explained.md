# Introduction
Ce document a pour but de vous expliquer en 5 minutes de lecture (et 5 autres de "digestion" ;) ) tout ce que vous devez savoir sur le XML et le XPATH utilisé par le Référentiel législatif de l'AN et les données en "OpenData" qui en sont issues.

Vous en saurez assez pour comprendre tout le XML et effectuer les requêtes XPATH vous permettant d'exploiter les données de l'OpenData.

XML et XPath sont des technologies riches et si vous voulez devenir un maitre Jedi dans ces matières vous devrez vous tourner vers d'autres sources d'information en ligne.
Cela ne devrait pas être nécessaire pour exploiter l'OpenData de l'Assemnblée nationale cependant.

# XML

Le XML se présente comme un format textuel dont voici un exemple.
Ce fichier XML serra la base de tous nos exemples subséquents.

```
<?xml version="1.0" encoding="UTF-8"?>
<export xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <organes>
        <organe xsi:type="OrganeParlementaire_Type">
            <uid>PO711218</uid>
            <codeType>MISINFO</codeType>
            <libelle>Formation des enseignants</libelle>
            <viMoDe>
                <dateDebut>2015-12-16</dateDebut>
                <dateAgrement xsi:nil="true"/>
                <dateFin>2016-10-05</dateFin>
            </viMoDe>
            <legislature>14</legislature>
            <secretariat>
                <secretaire xsi:nil="true"/>
                <secretaire xsi:nil="true"/>
            </secretariat>
        </organe>
        <organe xsi:type="OrganeParlementaire_Type">
            <uid>PO714518</uid>
            <codeType>ASSEMBLEE</codeType>
            <libelle>Assemble nationale</libelle>
            <viMoDe>
                <dateDebut>2016-12-16</dateDebut>
                <dateAgrement xsi:nil="true"/>
                <dateFin>2018-10-05</dateFin>
            </viMoDe>
            <legislature>14</legislature>
            <secretariat>
                <secretaire xsi:nil="true"/>
                <secretaire xsi:nil="true"/>
            </secretariat>
        </organe>
    </organes>
    <acteurs>
        <acteur>
            <uid>PA3445</uid>
            <etatCivil>
                <ident>
                    <nom>jean</nom>
                    <prenom>valjean</prenom>
                </ident>
            </etatCivil>
            <mandats>
                <mandat>
                    <uid>PM3455</uid>
                    <typeorgane>Assemblee</typeorgane>
                    <acteurRef>PA3445</acteurRef>
                </mandat>
            </mandats>
        </acteur>
    </acteurs>
</export>
```

## L'essentiel

### Arbre
un document XML est un arbre (il y a une "racine", unique, des "branches" et des "feuilles") de "noeuds". ces noeuds peuvent être de deux grands types : Les `Eléménts` et les `Attributs` (il y a d'autres tpes possibles mais vous ne les rencontrerez pas explicitement dans nos documents.)

## Balise

* Une balise est une chaine de charactère quelconque ('acteur', 'organe', 'ratatouille', 'poix123')
* Une balise peut être ouvrante comprise entre les symboles < et > (<acteur> <organe> etc ...) ou fermante, comprise entre les caractères < et /> (<acteur/>, <organe/>).
* Une balise peut enfin être "vide" ouvrante et fermante, comme ceci <acteur/>
* Toute balise ouvrante doit être assoiciée à une balise fermante (ou être une balise vide, ouvrante et fermante à la fois)
* Enfin, Les balises peuvent et doivent être imbriquée mais jamais se "chevaucher".

Exemple :

```xml
<racine>
<acteur><vide/></acteur>
<mandats></mandats>
</racine>
```


Mais jamais :

```xml
<racine>
<acteur>
  <mandats>
  </acteur>
</mandats>
</racine>
```


### élément
Un élément est la réunion d'une balise ouvrante et fermante et de tout ce qui se trouve entre.
Par exemple :

```xml
<secretariat>
    <secretaire xsi:nil="true"/>
    <secretaire xsi:nil="true"/>
</secretariat>
```
    
L'élément `secretariat` contient deux autres éléments `secretaire`

### Attribut

## Concepts "avancés"

Ces concepts sont inutiles pour comprenndre les données de l'Open Data mais vous en aurez besoin pour des usages avancés des données avec des outils sophisitiqués.

### Namespace

### schémas

# XPath

## L'essentiel

XPath est un langage de requếtage sur des documents au format XML.
C'est à dire qu'une expression XPath appliqué à un document XML retourne entre zéro et `n` noeuds (éléments ou attributs).

Une expression XPath simplement décrit le "chemin" pour accéder aux noeuds qu'elle souhaite récupérer, comme ceci :

`/export/organes/organe`

ou

`./organe`
    

Le résultat de l'expression XPath est l'ensemble des noeuds qui satisfont à l'expression.
La façon la plus simple d'apréhender une expression XPath est de la considérer comme un 'chemin' sélectionnant les noeuds correspondant au parcours de ce chemin depuils le point d'évaluation.

L'expression `/export/organes` limite ces noeuds aux fils de l'élément `Organes` eux même fils de la racine du document `export`.
Elle exprime ceci "retournez moi les noeuds appelés `organe`, fils d'un élément `organes` lui même fils de l'élément racine (`export`).
Les seuls noeud correspondants sont les deux éléments `organe` fils de `organes`, ce sont eux qui serront retournés, intégralement (avec leurs fils et tout leur contenu).

L'expression `./organe` retourne les noeuds `organe` fils `/` du noeud courant `.`.
En traduction pas à pas "du noeud ou vous êtes retournez moi les éléments fils de nom `organe`)

Son résultat dépend donc de l'endroit du fichier XML où elle est évaluée.
* Evaluée à la racine (`<export>`) cette expression ne retourne **rien** : Il n'y a pas d'élément `organe` fils de la racine (`<export>`).
* Evaluée sur l'élément `organes` elle retourne le même résultat que l'expression précédente :les deux éléments `organe` du document exemple qui sont bien fils directs de l'élément `organes`.

Mais peut-être voulez vous seulement le *premier* élément organe ?

`/export/organes/organe[1]`
    
ou le second

`/export/organes/organe[2]`

Vous pourriez aussi vouloir récupérer **tous** les éléments `organe`, peut importe où ils sont placés dans l'arborescence :

`//organe`
    
le symbole `//` veut dire 'n'importe où en dessous', fils direct, petit fils, petit petit fils, etc ...

## Un peu plus et ce sera assez ...

### Selecteur

Dans l'exemple `/export/organes/organe[1]` l'expression entre crochets `[]` est un selecteur.

Un sélecteur réduit le nombre de noeuds capturés par l'expression en posant une contrainte, un critère, un test sur les noeuds à cet endroit de l'expression.
Un simple nombre `n` indique de sélectionner le noeud de rang `n`, mais il est possible de construire des expressions plus puissantes.

```xml
/export/organes/organe[uid="PO714518"]
```
       
Sélectionne uniquement l'organe fils direct de ```/export/organes/``` possédant un fils `uid` de valeur "PO714518" si il existe.
Dans notre exemple il en existe un, le second.

`/export/organes/organe[.//dateDebut>"2016-01-01"]`
    
Sélectionne les organes fils de  `/export/organes/` ayant un sous élément  `dateDebut` postérieur au 1er janvier 2016.
Vous l'aurez remarqué l'expression de sélection est "enracinée" par défaut i.e. évaluée au point courant de l'expression, dans notre cas `/export/organes/`, et nous pouvons utiliser la notation `//` pour sélectionner n'importe quel élément descendant `dateDebut` à partir ce ce point.
En l'occurence l'élément date début est en fait situé en `./viMoDe/dateDebut` et nous aurious pu écrire l'expression comme ceci :

`/export/organes/organe[./viMoDe/dateDebut > "2016-01-01"]`

L'expression 'sélecteur' peut être n'importe quelle expression XPath valide qui traduit une condition booléenne.

## Any

Le symbole `*` représente n'importe quel élément.
 Ainsi l'expression :
 
`//*[uid="PO714518"]`
     
 représente n'importe quel élément possédant un fils direct  `uid` de valeur `PO714518`
 =>un organe dans notre exemple :
 

```xml
<organe xsi:type="OrganeParlementaire_Type">
                <uid>PO714518</uid>
                <codeType>ASSEMBLEE</codeType>
                ...
</organe>
```

`/*[uid="PO714518"]`

représente n'importe quel élément racine possédant un fils direct `uid` de valeur `PO714518`
=> aucun dans notre exemple


`//*[uid="PO714518"]`
 
représente n'importe quel élément racine possédant un descendant `uid` de valeur `PO714518`
 => le document racine 'export' en entier dans notre exemple.



###  Filtrer sur un attribut, xsi:nil ...

Enfin, pour tester la valeur d'un attribut il faut utiliser l'opérateur `@`

`//organe[@xsi:type="OrganeParlementaire_Type"]`

sélectionne tous les  organes ayant un attribut xsi:type de valeur "OrganeParlementaire_Type"
=> dans notre cas les deux éléments organes répondent à ce critère.

`//*[@xsi:nil="true"]`

retournera les 4 éléments `<secretaire>` **et** deux élémens `<dateAgrement>` dans notre exemple... vous devriez comprendre pourquoi à présent ;)

L'expression :

`//secretaire[@xsi:nil="true"]`

ne retournerait, elle, que les 4 éléments `<secretaire>`



# Et en Python ? lxml et co ...