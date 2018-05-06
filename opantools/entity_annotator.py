"""
    Ce module fournit un "annotation engine" ;).
    Le but est de compléter une "ref" (refOrgane, refActeur) dans un élément avec une information décrivant cette référence
    Par exemple

        <mandat>
        <uid>uidorgane1<uid>
        <refActeur>PA123</refActeur>
        </mandat>

        <mandat>
        <uid>uidorgane1<uid>
        <refActeur>PA123</refActeur>
        <refActeurDesc>Mr Paul Legendre</refActeur>
        <refActeurLongDesc>Mr Paul Legendre / 05-08-1985 </refActeur>
        </mandat>

D'autres formatages sont bien sur possibles.

Pour réaliser cela, ce module créé une "base en mémoire" des acteurs mandats organes et autres éléments annotables

"""

from opantools.file_loader import get_src_file_path
from opantools.ref_formater import format_entity
from opantools.xml_tools import fragparse


class EntityDescs:

    entity_file_map = {
        "PA": ("acteur", ("AMO20_dep_sen_min_tous_mandats_et_organes_XIV.xml", "AMO30_tous_acteurs_tous_mandats_tous_organes_historique.xml")),
        "PM": ("mandat", "AMO30_tous_acteurs_tous_mandats_tous_organes_historique.xml"),
        "PO": ("organe", "AMO30_tous_acteurs_tous_mandats_tous_organes_historique.xml"),
        # "amdt": ("amendement",),
    }

    entity_db = {}

    def __init__(self, format_form_name='default'):
        self.formating_form_name = format_form_name

    def db_load(self, entity_name, src_file_names):
        entity_db = self.entity_db
        if isinstance(src_file_names, str):
            src_file_names = (src_file_names,)
        for src_file_name in src_file_names:
            file_to_load = get_src_file_path(src_file_name)
            for fragxml in fragparse(file_to_load, entity_name):
                uid = fragxml[0].text
                entity_db[uid] = format_entity(fragxml, form_name=self.formating_form_name)

    def get_entity_from_memdb(self, uid, silent_fail=False):
        entity_db = self.entity_db
        ent = entity_db.get(uid)
        if ent is None:
            entity_code = uid[:2]
            element_name, src_file_name = self.entity_file_map.get(entity_code, (None, None))
            if element_name:
                self.db_load(element_name, src_file_name)
            else:
                if not silent_fail:
                    raise ValueError("je n'ai pas de source pour charger des [{}], mon dictionnaire est [{}]".format(entity_code, self.entity_file_map))
        ent = entity_db.get(uid)
        if not silent_fail and ent is None:
            raise ValueError("[{}] non trouvé dans la base des entités, le fichier source ne contient pas cet uid".format(uid))
        return ent

    def prefetch(self, entity_names=None):
        for entity_code, entity_info in self.entity_file_map.items():
            entity_name, entity_filenames = entity_info
            if entity_names is None or entity_name in entity_names:
                self.db_load(entity_name, entity_filenames)


if __name__ == "__main__":
    desc_map = EntityDescs(format_form_name='long')
    desc_map.prefetch()
    ent_PA = desc_map.get_entity_from_memdb('PA608310')
    print(ent_PA)
    ent_PA = desc_map.get_entity_from_memdb('PA429892')
    print(ent_PA)
    ent_PO = desc_map.get_entity_from_memdb('PO698927')
    print(ent_PO)
    ent_PM = desc_map.get_entity_from_memdb('PM645293')
    print(ent_PM)



