import heapq

from opantools.common_XPath import ACTEUR_MANDATS
from opantools.file_loader import get_src_file_path
from opantools.ref_formater import format_entity
from opantools.xml_tools import fragparse

def count_mandats_par_dep_cb(xml, result_dict):
    if xml.tag == "acteur":
        idt = format_entity(xml)
        result_dict[idt] = len(ACTEUR_MANDATS(xml))
    return result_dict


def most_nominated(src_file, limit=5):
    results = dict()
    # nous devons épuiser le générateur 'fragparse' pour peupler  'results'
    for item, result in fragparse(src_file, tags="acteur", callback=count_mandats_par_dep_cb, cb_data=results):
        pass
    mlist = [(mdcount, person) for (person, mdcount) in results.items()]
    # réorganisation de la list en heapq, cf https://rockie-yang.gitbooks.io/python-cookbook/content/ch1/collection_heapq.html
    heapq.heapify(mlist)
    print("Les {} acteurs ayant le plus de mandats {}".format(limit, heapq.nlargest(limit, mlist)))
    print("Les {} acteurs ayant le moins de mandats {}".format(limit, heapq.nsmallest(limit, mlist)))


def main(src_file_name):
    src_file_path = get_src_file_path(src_file_name)
    most_nominated(src_file_path, limit=10)


if __name__ == '__main__':
    main(r"AMO20_dep_sen_min_tous_mandats_et_organes_XIV.sample.xml")
