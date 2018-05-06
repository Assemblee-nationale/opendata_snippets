import os
import copy
from lxml import etree


def fragparse(xml_file, tags, callback=None, cb_data= None, empty_purge=False, remove_blank_text=True):
    """
    Générateur fournissant l'itération sur les éléments (lxml.etree.Element)
    défini par les ``tags`` sélectionnés. Les éléments sont éventuellement
    préalablement traités par une fonction de ``callback`` si fournie.

    Sachant que cette recherche de fragments peut explorer des fichiers XML de 10Mo
    ou plus, la stratége ici choisie consiste à utiliser le procédé le plus économe possible
    de ressources mémoire : un parseur de type `SAX`.

    Usage:

    ```
    for item in fragparse(src_file, tags=['toto',], callback=mafunc):
        print(etree.tostring(item))

    ou

    for (item, result_dic) in fragparse(src_file, tags=['toto',], callback=mafunc, cb_data={} ):
        print(etree.tostring(item), result_dic)
    ```

    .. attention::

        cette fonctionne retourne **une** valeur à chaque itération (le fragment de XML portant un des noms d'éléments cités dans `tags`) **si**
        :param:`cb_data` est à `None`, mais elle retourne **deux** valeurs sinon : le fragment xml **et** la valeur courante de :param:`cb_data`.


    .. attention::

       Du fait d'un bug dans lxml compilé sous CentOS, il est indispensable d'ouvrir le
       fichier ``xml_file`` avec ``io.open`` en mode ``rb`` et non avec le builtin ``open``.


    Args:
        xml_file (file or str) : objet de type ``file`` ou assimilé, ou chemin de fichier (str)
        tags (iterable): séquence de noms de tags à traiter
        callback(func): fonction à un paramètre (un élément ``lxml.etree.Element``)
        cb_data (any): cb_data sera passé à la fonction callback et retourné par elle, cela peut être une liste, un dictionnaire, une valeur simple que vous
            voulez passer à votre fonction en plus du "noeud" courant (un des noeuds du flux dont le nom d'élément correspond à un des tags
            dans :param:`tags`)
            Votre fonction  :param:`callback` doit retourner le nouveau contenu de cette variable qui sera passée lors de l'appel suivant.
            Cela vous permet de construire un cache, une somme ou ce que vous souhaitez, Si vous ne souhaitez pas utiliser cette capacité,
             la valeur par défaut de `None` pour :param:`cb_data` est valide.
            La valeur courante de :param:`cb_data` est retournée lors de chaque "yield" **SI** elle est différente de None
            Autrement dit ces deux appels sont valides :
              *  for item in fragparse(src_file, tags=['toto',], callback=mafunc): ...
              *  for (item, result_dic) in fragparse(src_file, tags=['toto',], callback=mafunc, cb_data={} ): ...
            mais celui ci ne l'est **pas**
                for item in fragparse(src_file, tags=['toto',], callback=mafunc, cb_data={} ): ...
                car si cb_data est différent de None la fonction retourne deux valeurs à chaque itération.
        empty_purge: suppression des éléments vides et sans attribut
        remove_blank_text: suppression des noeud contenant du texte vide (ils ne sont pas retournés du tout)

    Returns:

    """

    level = 0
    match_inner = False
    if isinstance(tags, str):
        tags = (tags,)
    for event, element in etree.iterparse(xml_file, events=('start', 'end'), remove_blank_text=remove_blank_text):
        if event == 'start':
            level += 1
            if not match_inner and element.tag in tags:
                match_inner = element.tag
                match_level = level
        else:
            # event == 'end' (forcément)
            if element.tag == match_inner and match_level == level:
                match_inner = False
                elt_copy = copy.deepcopy(element)
                if callable(callback):
                    cb_data = callback(elt_copy, cb_data)
                elt_copy = elt_copy if not empty_purge else purge_empty(elt_copy)
                if cb_data:
                    yield (elt_copy, cb_data)
                else:
                    yield elt_copy
                element.clear()
            level -= 1
        if not match_inner:
            element.clear()


def purge_empty(xml):
    assert isinstance(xml, etree._Element) or isinstance(xml, etree._ElementTree)
    for event, element in etree.iterwalk(xml, events=("end",)):
        assert isinstance(element, etree._Element)
        if len(element) == 0 and len(element.attrib) == 0 and element.text is None:
            element.getparent().remove(element)
    return xml

