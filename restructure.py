"""
Un exemple de restructuration du flux de données pour produire un fichier CSV ad-hoc.
Cet exemple utilise une logique "DOM" c'est à dire que tout le fichier XML est chargé en mémoire et explorable en XPath
"""

import os
from lxml import etree
import csv

#from profiler import do_profile

SCRIPT_ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_SRC_DIR = os.path.join(SCRIPT_ROOT_DIR, 'data_src')


UID = etree.ETXPath(r"./uid")
ACTEUR_MANDATS = etree.ETXPath(r"./mandats/mandat")
ORGANES = etree.ETXPath(r".//organe")
ORGANE_REF = etree.ETXPath(r".//organeRef")
TYPE_ORG_FROM_ORGANE = etree.ETXPath(r".//typeOrgane")
ACTEUR_IDENT = etree.ETXPath(r".//etatCivil/ident")
ACTEURS = etree.ETXPath(r".//acteur")
DNAIS_FOR_ACTEUR = etree.ETXPath(r".//dateNais")
DEBUT_MANDAT = etree.ETXPath(r".//dateDebut")
FIN_MANDAT = etree.ETXPath(r".//dateFin")
ORGANE_BY_UID = etree.ETXPath(r"/export/organes/organe[uid=$uid]")


def format_acteur(acteur_xml):
    uid = acteur_xml[0].text
    ident = ACTEUR_IDENT(acteur_xml)[0].getchildren()
    idt = "[{}] {} {} {}".format(uid, ident[0].text, ident[1].text, ident[2].text)
    return idt


def extract2csv_pure_xpath(src_file_path):
    parsed = etree.parse(src_file_path)
    acteurs = ACTEURS(parsed)
    for acteur in acteurs:
        act = format_acteur(acteur)
        dnaiss = DNAIS_FOR_ACTEUR(acteur)[0].text.replace('-', '/')
        line = [act + '-' + dnaiss,]
        mandats = ACTEUR_MANDATS(acteur)
        mandats_parts = []
        for mandat in mandats:
            uid_mandat = mandat[0].text
            organe_ref = ORGANE_REF(mandat)[0].text
            type_mandat = TYPE_ORG_FROM_ORGANE(mandat)[0].text
            organe = ORGANE_BY_UID(parsed, uid=organe_ref)[0]
            mdt_deb = DEBUT_MANDAT(mandat)[0].text.replace('-', '/')
            mdt_fin = FIN_MANDAT(mandat)[0].text
            mdt_fin = mdt_fin.replace('-', '/') if mdt_fin else ""
            # mandat_line = "{}-{}-{}-{}-{}".format(uid_mandat, organe[2].text, mdt_deb, mdt_fin, type_mandat)
            mandat_line = "-".join((uid_mandat, organe[2].text, mdt_deb, mdt_fin, type_mandat))
            mandats_parts.append(mandat_line)
        yield (line, ";".join(mandats_parts))


def extract2csv_full_cache(src_file_path):
    parsed = etree.parse(src_file_path)
    organes = ORGANES(parsed)
    # on se construit un dictionnaire des organes pour rechercher ceux-ci plus vite à partie de leur uid.
    # xml[0].text est l'uid de l'élément les documents du référentiel on toujours un premier élément fils de la racine nommé "uid"
    # une façon plus "propre" mais légérement moins rapide de faire cela serait de faire UID(organe_fragment)[0].text
    # comme ceci :
    # organes_map = {UID(organe_fragment)[0].text: organe_fragment for organe_fragment in organes}
    organes_map = {organe_fragment[0].text: organe_fragment for organe_fragment in organes}
    acteurs = ACTEURS(parsed)
    for acteur in acteurs:
        act = format_acteur(acteur)
        dnaiss = DNAIS_FOR_ACTEUR(acteur)[0].text.replace('-', '/')
        line = [act + '-' + dnaiss, ]
        mandats = ACTEUR_MANDATS(acteur)
        mandats_parts = []
        for mandat in mandats:
            uid_mandat = mandat[0].text
            organe_ref = ORGANE_REF(mandat)[0].text
            type_mandat = TYPE_ORG_FROM_ORGANE(mandat)[0].text
            organe = organes_map[organe_ref]
            mdt_deb = DEBUT_MANDAT(mandat)[0].text.replace('-', '/')
            mdt_fin = FIN_MANDAT(mandat)[0].text
            mdt_fin = mdt_fin.replace('-', '/') if mdt_fin else ""
            # mandat_line = "{}-{}-{}-{}-{}".format(uid_mandat, organe[2].text, mdt_deb, mdt_fin, type_mandat)
            mandat_line = "-".join((uid_mandat, organe[2].text, mdt_deb, mdt_fin, type_mandat))
            mandats_parts.append(mandat_line)
        yield (line, ";".join(mandats_parts))


def main(src_file_name):
    src_file = os.path.join(DATA_SRC_DIR, src_file_name)
    out_dir_path = os.path.join(SCRIPT_ROOT_DIR, "out_dir")
    if not os.path.exists(out_dir_path):
        os.mkdir(out_dir_path)
    outfile_path = os.path.join(out_dir_path,  "output.csv")
    with open(outfile_path, "w", encoding='utf-8') as f:
        w = csv.writer(f)
        for line in (extract2csv_pure_xpath(src_file)):
            print(line)
            w.writerow(line)
    print("Done")


def timable(src_file_name):
    src_file = os.path.join(DATA_SRC_DIR, src_file_name)
    for line in extract2csv_full_cache(src_file):
        print(line)
    print("done")


if __name__ == "__main__":
    timable(r"AMO20_dep_sen_min_tous_mandats_et_organes_XIV.sample.xml")
    # main(r"AMO20_dep_sen_min_tous_mandats_et_organes_XIV.sample.xml")

