""""
 Ce module est un receuil d'expression XPath exprimée en ETXPath de la librairie lxml représentant autant des exemples que des requêtes courantes sur
  les entités du référentiel présente dans les fichiers OpenData.

L'outil recommandé pour parcourir l'arbre est ETXPath dans la librairie lxml.

 Selon où vous utilisez le XPath le "." est important car il "ancre" votre requête à partir du noeud courant.
 Par exemple si vous chargez un fichier XML comme ceci : parsed = etree.parse(mon_fichier)
 et que vous récupérez un élément X de parsed, par exemple x=parsed[100] faire x.xpath("//organe") ne vous donnera pas
 tous les éléments "organe" fils de "x" mais tous les élément "organe" présents dans le document dont X est un noeud, en l'occurence 'parsed'.
 Dans notre cas cela sera 5 000, 6 000, 10 000 noeuds organes ou plus ;)
 Pour avoir les fils 'organe' de x vous devez faire x.xpath(".//organe"), ou x.xpath("./organe") si vous ne voulez que les "organe" fils directs de x.
 En régle générale xpath(".//organe") est meilleur car il fonctionne aussi bien depuis la racine que sur n'importe quel noeud et donne
 dans les deux cas le résultat escompté.
"""

from lxml import etree

"""Les "constantes" suivantes sont des fonctions retournant le résultat de l'expression XPath
 passée en paramêtre quand elle sont appliquée à un fragment xml.
 Ces fonctions retournent une **liste** de résultat. Quand nous sommes certains qu'il n'y a qu'un résultat nous pouvons faire ceci par exemple :
 UID(fragment_xml)[0] mais attention, si il est possible que l'expression ne renvoi aucun résultat, UID(fragment_xml) retournera None et
 l'expression UID(fragment_xml)[0] générera une exception.
 En ce cas il vaut mieux écrire ceci :
 uid_content = UID(fragment_xml)
 uid_content = uid_content[0].text if uid_content is not None else None
 uid_content vaudra la valeur de l'uid ou None si fragment_xml ne comporte pas de premier élément fils de nom uid OU si cet élément 'uid' est vide.
"""

#######################################################################
# Sur tous les éléments "concept" (acteur, organe, amendement, etc ..)#
#######################################################################

UID = etree.ETXPath(r"./uid/text()")
UID_FUZZY = etree.ETXPath(r".//uid/text()")

#########################
# sur un élément acteur #
#########################

# L'élément "ident" d'un élément "acteur" (qui contient en sous éléments le petit état civil d'un acteur (nom, prénom, classement alpha)
ACTEUR_IDENT_ELEM = etree.ETXPath(r".//etatCivil/ident")
ACTEUR_ETATCIV_ELEM = etree.ETXPath(r".//etatCivil")
ACTEUR_DATNAIS_ELEM = etree.ETXPath(r".//etatCivil/dateNais/text()")
# L'élément "mandats" d'un élément "acteur"
ACTEUR_MANDATS = etree.ETXPath(r"./mandats/mandat")

#########################
# sur un élément mandat #
#########################

# le sous élément organe_ref d'un mandat (qui pointe sur le ou les (dans le seul cas des missions) organes sur lequel porte le mandat
MANDAT_ORGANE_REF = etree.ETXPath(r".//organeRef/text()")
# la nature d'un mandat qui est aussi le type de l'organe sur lequele portee le mandat
# (ASSEMBLEE pour un mandat de député, CMP pour un commission paritaire, etc.)
MANDAT_TYPE_ORGANE = etree.ETXPath(r"./typeOrgane/text()")
# Le type fonctionnel (parlementaire, externe, etc ...) d'un mandat
# Il y a un problème dans les données et certains mandats ont un attribut type et non xsi:type (correction urgente en cours)
MANDAT_TYPE_MANDAT = etree.ETXPath(r'./@{http://www.w3.org/2001/XMLSchema-instance}type|./@type')

MANDAT_DATEDEBUT = etree.ETXPath(r'./dateDebut/text()')
MANDAT_DATEFIN = etree.ETXPath(r'./dateFin/text()')
MANDAT_DATEPUBLICATION = etree.ETXPath(r'./datePublication/text()')


#########################
# sur un élément organe #
#########################
ORGANE_TYPE_ORGANE = etree.ETXPath(r"./codeType/text()")
ORGANE_LIBELLE = etree.ETXPath(r"./libelle/text()")

#########################
# sur un élément Question #
#########################
QUESTION_NUMERO = etree.ETXPath(r"/question/identifiant/numero/text()")
QUESTION_UID = etree.ETXPath(r"/question/uid/text()")
QUESTION_TYPE_QUESTION = etree.ETXPath(r"/question/type/text()")

QUESTION_MININT = etree.ETXPath(r"/question/minInt/abrege/text()")
# retournera une liste (de dénomination des ministères auquels la question a été attribuée
QUESTION_MINATTRIB = etree.ETXPath(r"/question/minAttribs/minAttrib/denomination/abrege/text()")
