import os
import copy
from lxml import etree
import heapq

SCRIPT_ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_SRC_DIR = os.path.join(SCRIPT_ROOT_DIR, 'data_src')

UID = etree.ETXPath(r"/*/uid")
MANDATS = etree.ETXPath(r"//mandats/mandat")
IDENT = etree.ETXPath(r"/acteur/etatCivil/ident")


def fragparse(xml_file, tags, callback=None, empty_purge=False, remove_blank_text=True):
    """Générateur fournissant l'itération sur les éléments (lxml.etree.Element)
    défini par les ``tags`` sélectionnés. Les éléments sont éventuellement
    préalablement traités par une fonction de ``callback`` si fournie.

    Sachant que cette recherche de fragments peut explorer des fichiers XML de 10Mo
    ou plus, la stratége choisie consiste à utiliser le procédé le plus économe possible
    de ressources mémoire.

    :param xml_file: objet de type ``file`` ou assimilé, ou chemin de fichier (str)
    :param tags: séquence de noms de tags à traiter
    :param callback: fonction à un paramètre (un élément ``lxml.etree.Element``)
    :param empty_purge: suppression des éléments vides et sans attribut
    :param remove_blank_text: suppression des espaces entourant le texte

    .. attention::

       Du fait d'un bug dans lxml compilé sous CentOS, il est indispensable d'ouvrir le
       fichier ``xml_file`` avec ``io.open`` en mode ``rb`` et non avec le builtin ``open``.
    """
    level = 0
    match_inner = False
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
                    cb_result = callback(elt_copy)
                    # in case the callback does not return the fragment we keep the original fragment (potentially modified by the callback)
                    elt_copy = cb_result if len(cb_result) else elt_copy
                yield elt_copy if not empty_purge else purge_empty(elt_copy)
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


def split_element_names(in_flux, out_dir, elements_names, cb_func=None):
    """
        Cette fonction illustre la restructruration d'un flux d'entrée "Acteur/Mandat/Organes" présentant d'un seul bloc, tous les organes, puis
     les acteurs avec leurs mandats inclus.
     Le resultat est deux sous répertoire de out_dir, out_dir/organes et out_dir/acteurs contenant les deux sous flux séparés aec un fichier par
     élément organe ou acteur. Les fichiers sont de nom "uid.xml"
     Le répertoire out_dir est créé si il n'existe pas, les fichiers de sortie sont ajoutés ou écrasent les fichiers éventuellement déja
     présents dans les répertoires de destination (merge implicite des contenus de répertoire, pas des fichiers bien sur)
    Args:
        in_flux (string): le chemin complet du fichier à analyser.
        out_dir (string: le répertoire de destination des fichiers divisés
        elements_names (iterable) : liste des nom d'éléments à extraire du flux entrant dans des fichiers séparés
        cb_func (function) : fonction facultative appliquée à chaque élément "extrait"

    Returns (int): nombre de fichiers créés

    """
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    for fragment_element in elements_names:
        outfile_path = os.path.join(out_dir, fragment_element)
        if not os.path.exists(outfile_path):
            os.makedirs(outfile_path)

    for index, frag_xml in enumerate(fragparse(in_flux, elements_names, callback=cb_func)):
        # print("%s" % (xml.tag))
        kind = frag_xml.tag
        uid = frag_xml[0].text
        outfile_path = os.path.join(out_dir, kind, uid + ".xml")
        with open(outfile_path, "w", encoding='utf-8') as ofd:
            ofd.write(etree.tostring(frag_xml, encoding='unicode', pretty_print=True))
    return index-1


# closure sur result_dict
def accumulator(result_dict):
    def accumulate_cb(xml):
        tag = xml.tag
        if tag in result_dict:
            result_dict[tag] += 1
        else:
            result_dict[tag] = 0
        return xml
    return accumulate_cb


def format_acteur(acteur_xml):
    uid = acteur_xml[0].text
    ident = IDENT(acteur_xml)[0].getchildren()
    idt = "[{}]-{} {} {}".format(uid, ident[0].text, ident[1].text, ident[2].text)
    return idt


# closure sur result_dict
def count_mandat(result_dict):
    def accumulate_cb(xml):
        if xml.tag == "acteur":
            idt = format_acteur(acteur_xml=xml)
            result_dict[idt] = len(MANDATS(xml))
        return xml
    return accumulate_cb


def ex1_split_flux_in_files(src_file):
    elements_names = ('organe', 'acteur')
    out_dir_path = os.path.join(SCRIPT_ROOT_DIR, "out_dir")
    count = split_element_names(src_file, out_dir_path, elements_names=elements_names)
    print("{} eléments traités".format(count))
    print("les fichiers sont ici {}".format(out_dir_path))


def ex2_count_by_elem_types(src_file):
    results = dict()
    elements_names = ('organe', 'acteur')
    # nous devons épuiser le générateur 'fragparse' pour peupler  'results'
    _ = [item for item in fragparse(src_file, tags=elements_names, callback=accumulator(result_dict=results))]
    print("Decompte par type d'élément [{}] dans le flux source [{}]".format(elements_names, results))


def ex3_most_nominated(src_file, largest_smallest_count=5):
    """
    Calculons le nombre de mandats par acteur (et non ce calcul n'a **rien** à voir avec le cumul des mandats, référez vous à la définition
    d'un mandat dans le Référentiel/Opendata pour savoir pourquoi.
    De même certains députés sont réélus ...
    Returns: None
    """
    results = dict()
    elements_names = ('organe', 'acteur')
    # nous devons épuiser le générateur 'fragparse' pour peupler  'results'
    _ = [item for item in fragparse(src_file, tags=elements_names, callback=count_mandat(result_dict=results))]
    # Construction d'un liste de tuples (nombre_de_mandats, acteurs)
    mlist = [(mdcount, person) for (person, mdcount) in results.items()]
    # réorganisation de la list en heapq, cf https://rockie-yang.gitbooks.io/python-cookbook/content/ch1/collection_heapq.html
    heapq.heapify(mlist)
    print("Les {} acteurs ayant le plus de mandats {}".format(largest_smallest_count, heapq.nlargest(largest_smallest_count, mlist)))
    print("Les {} acteurs ayant le moins de mandats {}".format(largest_smallest_count, heapq.nsmallest(largest_smallest_count, mlist)))


def main(src_file_name):
    src_file = os.path.join(DATA_SRC_DIR, src_file_name)
    # Décommentez la ligne suivante pour activer le découpage du flux AM020 en éléments distincts
    # ex1_split_flux_in_files(src_file)
    ex2_count_by_elem_types(src_file)
    ex3_most_nominated(src_file)


if __name__ == "__main__":
    main("AMO20_dep_sen_min_tous_mandats_et_organes_XIV.sample.xml")








