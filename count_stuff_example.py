import os

from xml_tools import fragparse

SCRIPT_ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_SRC_DIR = os.path.join(SCRIPT_ROOT_DIR, 'data_src')


def count_by_elem_types_cb(xml, result_dic):
    """
    Cette fonction est destinée à être transmise à la fonction :py:func:xml_tools.frag_parse avec le fragment XML courant et un dictionnaire

    Elle compte tous les nom d'éléments racine différents des fragments que l'on lui passe en accumulant la somme pour chaque dans :param:result_dic
    si vous lui passez successivement des fragments de XML de ce type :
    <organe><toto/>..</organe>,
    <organe><titi/>...</organe>,
    <acteur>...</acteur>
    Elle vous retournera
    {'acteur':1, 'organe':2}
    Args:
        xml: un fragment de XML
        result_dic: l'état courant des compteurs
    Returns: result_dic

    """
    tag = xml.tag
    if tag in result_dic:
        result_dic[tag] += 1
    else:
        result_dic[tag] = 0
    return result_dic


def count_by_elem_types(src_file, elements_names):
    results = dict()
    # nous devons épuiser le générateur 'fragparse' pour peupler  'results'
    for item, result in fragparse(src_file, tags=elements_names, callback=count_by_elem_types_cb, cb_data=results):
        pass
    print("Decompte par type d'élément [{}] dans le flux source [{}]".format(elements_names, results))


def main(src_file_name):
    src_file = os.path.join(DATA_SRC_DIR, src_file_name)
    out_dir_path = os.path.join(SCRIPT_ROOT_DIR, "out_dir")
    if not os.path.exists(out_dir_path):
        os.mkdir(out_dir_path)
    count_by_elem_types(src_file, elements_names=('organe', 'acteur'))
    count_by_elem_types(src_file, elements_names=('mandat', 'acteur'))
    count_by_elem_types(src_file, elements_names='ident')


if __name__ == '__main__':
    main(r"AMO20_dep_sen_min_tous_mandats_et_organes_XIV.sample.xml")

