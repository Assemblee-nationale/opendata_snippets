"""
Ce module / script python vous permet de diviser un fichier aggrégé de l'opendata en autant de fichiers individuels, un par entité (i.e. un par uid)

Exemple :
Sur un fichier source `source.xml` structuré comme ceci
<export >
    <organes>
        <organe>
        <uid>uidorgane1<uid>
        ...
        </organe>
    </organe>
    <acteurs>
        <acteur>
            <uid>uidacteur1<uid>
            ...
        <acteur>
        <acteur>
            <uid>uidacteur2<uid>
            ...
        </acteur>
    </acteurs>
</export>

Appeler

    split_element_names('source.xml','out_dir',  ['acteur','organe'])

produit le résultat suivant sur le système de fichier :
     out_dir
      --organe
      ----- uidorgane1.xml
      ...
      --acteur
      ------ uidacteur1.xml
      ------ uidacteur2.xml
      ...

    où les fichiers uidorgane1.xml, uidacteur1.xml, uidacteur2.xml contiennent le xml correspondant à organe1, acteur1, acteur2 issu du fichier source.

Il est également possible de passer une fonction "callback" lors de l'appel de :py:func:`split_element_names` pour modiifier le XML de chaque élément
avant sa sauvegarde sur le disque.

"""
import os

from lxml import etree

from opantools.xml_tools import fragparse

SCRIPT_ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_SRC_DIR = os.path.join(SCRIPT_ROOT_DIR, 'data_src')


def split_element_names(in_flux, out_dir, elements_names, cb_func=None, uid_xpath=None):
    """
    Cette fonction illustre la restructruration d'un flux d'entrée, par exemple "Acteur/Mandat/Organes" présentant d'un seul bloc, tous les organes,
    puis les acteurs avec leurs mandats inclus.
     Le resultat est deux sous répertoire de out_dir, out_dir/organes et out_dir/acteurs contenant les deux sous flux séparés aec un fichier par
     élément organe ou acteur. Les fichiers sont de nom "uid.xml"
     Le répertoire out_dir est créé si il n'existe pas, les fichiers de sortie sont ajoutés ou écrasent les fichiers éventuellement déja
     présents dans les répertoires de destination (merge implicite des contenus de répertoire, pas des fichiers bien sur)
    Args:
        in_flux (string): le chemin complet du fichier à analyser.
        out_dir (string: le répertoire de destination des fichiers divisés
        elements_names (iterable) : liste des nom d'éléments à extraire du flux entrant dans des fichiers séparés
        cb_func (function) : fonction facultative appliquée à chaque élément "extrait" avant sauvegarde
        uid_xpath: xpath utilisé pour calculer le nom du fichier de sortie, si uid_xpath est None il est assumé que le fragment XML est un
         élément du référentiel bien formé et donc que le premier fils de sa racine est son élément ` uid`, qui est alors utilisé pour générer le nom
         de fichier de sortie.

    Returns (int): nombre de fichiers créés

    """
    # si on ne nous passe qu'une chaine pour elements_names, on considère que c'est le seul nom d'élément
    # et on en fait une liste d'un seul élément pour la suite
    if isinstance(elements_names, str):
        elements_names = (elements_names,)
    # # on créé le répertoires de sortie
    # if not os.path.exists(out_dir):
    #     os.makedirs(out_dir)
    # on "compile" le xpatch passé en paramètre si besoin
    if uid_xpath is not None:
        uid_xpath = etree.ETXPath(uid_xpath)

    for fragment_element in elements_names:
        outfile_path = os.path.join(out_dir, fragment_element)
        if not os.path.exists(outfile_path):
            os.makedirs(outfile_path)
    index = 0
    for index, frag_xml in enumerate(fragparse(in_flux, elements_names, callback=cb_func)):
        xml_tag = frag_xml.tag
        if uid_xpath is None:
            uid = frag_xml[0].text
        else:
            uid = uid_xpath(frag_xml)[0].text
        outfile_path = os.path.join(out_dir, xml_tag, uid + ".xml")
        with open(outfile_path, "w", encoding='utf-8') as out_fd:
            out_fd.write(etree.tostring(frag_xml, encoding='unicode', pretty_print=True))
    return index+1 if index else 0


def process(src_file_name, elements_names, uid_xpath=None):
    src_file = os.path.join(DATA_SRC_DIR, src_file_name)
    out_dir = os.path.join(SCRIPT_ROOT_DIR, "out_dir")
    core_src_filename = os.path.splitext(os.path.basename(src_file))[0]
    out_dir_path = os.path.join(out_dir, core_src_filename)
    count = split_element_names(src_file, out_dir_path, elements_names=elements_names, uid_xpath=uid_xpath)
    print("{} eléments traités".format(count))
    print("les fichiers sont ici {}".format(out_dir_path))


if __name__ == "__main__":
    # ceci sépare les comptes rendus en autant de fichiers individuels nommé selon la "dateSeance". Mais le flux syceron est 'artistique' et ne suit
    # aucun schéma dateSeance peut devenir DateSeance ou Date_Seance ou date_seance, c'est, en gros, n'importe quoi, et en l'occurence ce n'est pas
    # une date mais un timestamp (date+heure) et donc chaque séance est uniquement identifiée par cet élément
    process(r"SyceronBrut.xml", elements_names="CompteRendu", uid_xpath=".//dateSeance|.//DateSeance")
    # La ligne suivante extrait les "métadonnées" de chaque compte rendu de séance sous un nom correspondant à la "date" séance
    # process(r"SyceronBrut.xml", "CompteRendu", elements_names=('Metadonnees',), uid_xpath='.//dateSeance|.//DateSeance')
    process(r"AMO20_dep_sen_min_tous_mandats_et_organes_XIV.sample.xml", elements_names=('acteur', 'organe'))
    print("done processing")








