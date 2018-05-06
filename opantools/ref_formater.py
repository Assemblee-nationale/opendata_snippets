"""
** Here be DRAGONS **
ce code n'est pas du code pour débutant en python si son usage est simple la compréhension de son fonctionnement nécessite
une très bonne connaissance de python.

Par contre, son usage et son extension pour de nouvelles présentation ou de nouveau fragments de XML, devrait être 'simple' :

Si vous voulez ajouter une nouvelle présentation pour un type de fragment XML, vous n'avez qu'a ajouter une  méthode

 def xxx_form(xml):
 qui doit retourner le formatage que vous souhaitez.

 Si vous voulez ajouter une présentation à des types d'éléments qui ne sont pas gérés, vous devez simplement ajouter une classe  nommée
 FormatXXXX ou XXXX est le nom du tag racine de l'élément que vous souhaitez formater (exemple: class FormatActeur(FormatBaseKlass):).
 Ensuite ajoutez simplement une méthode short_form, statique, et autant de méthodes xxx_form que de besoin.
"""

from opantools.common_XPath import ACTEUR_IDENT_ELEM, ACTEUR_DATNAIS_ELEM
from opantools.common_XPath import MANDAT_TYPE_ORGANE, MANDAT_TYPE_MANDAT, MANDAT_ORGANE_REF, MANDAT_DATEDEBUT, MANDAT_DATEFIN
from opantools.common_XPath import ORGANE_TYPE_ORGANE, ORGANE_LIBELLE
from opantools.common_XPath import UID

FORMS = ('default', 'short', 'long', 'extended')


def _get_formater_klass_for_fragment(xml):
    tag = xml.tag
    class_name = 'Format' + tag.capitalize()
    klass = globals().get(class_name)
    if klass is not None:
        return klass
    raise ValueError("il n'y a pas de classe de formatage [(Format{})] définie dans le module pour un élément {}.\n ".format(tag, tag))


class FormatBaseKlass:

    @staticmethod
    def default_form(xml):
        klass = _get_formater_klass_for_fragment(xml)
        check_xml = getattr(klass, 'check_xml', None)
        if check_xml:
            klass.check_xml(xml)
        return klass.short_form(xml)


class FormatActeur(FormatBaseKlass):

    @staticmethod
    def check_xml(xml):
        assert xml.tag == "acteur", "format_acteur doit recevoir un fragment de XML d'un acteur, vous avez passé un {} ".format(xml.tag)

    @staticmethod
    def short_form(acteur_xml):
        (uid,) = UID(acteur_xml)
        ident = ACTEUR_IDENT_ELEM(acteur_xml)[0].getchildren()
        acteur_repr = "[{}] {} {} {}".format(uid, ident[0].text, ident[1].text, ident[2].text)
        return acteur_repr

    @staticmethod
    def long_form(acteur_xml):
        (uid,) = UID(acteur_xml)
        ident = ACTEUR_IDENT_ELEM(acteur_xml)[0].getchildren()
        date_naiss_tmp = ACTEUR_DATNAIS_ELEM(acteur_xml)
        (date_naiss,) = date_naiss_tmp if date_naiss_tmp else ("",)
        acteur_repr = "[{}]|{} {} {}|{}".format(uid, ident[0].text, ident[1].text, ident[2].text, date_naiss)
        return acteur_repr


class FormatOrgane(FormatBaseKlass):

    @staticmethod
    def check_xml(xml):
        assert xml.tag == "organe", "format_organe doit recevoir un fragment de XML pour un organe, vous avez passé un {} ".format(xml.tag)

    @staticmethod
    def short_form(organe_xml):
        (uid,) = UID(organe_xml)
        (nom_organe, ) = ORGANE_LIBELLE(organe_xml)
        (type_organe,) = ORGANE_TYPE_ORGANE(organe_xml)
        organe_dec = "[{}]|{}|({})".format(uid, nom_organe, type_organe)
        return organe_dec

    @staticmethod
    def long_form(organe_xml):
        return FormatOrgane.short_form(organe_xml)


class FormatMandat(FormatBaseKlass):

    @staticmethod
    def check_xml(xml):
        assert xml.tag == "mandat", "FormatMandat doit recevoir un fragment de XML pour un Mandat, vous avez passé un {} ".format(xml.tag)

    @staticmethod
    def long_form(mandat_xml):
        (mandat_uid,) = UID(mandat_xml)
        organes_refs = MANDAT_ORGANE_REF(mandat_xml)
        organes_desc = ','.join(organes_refs)
        (mandat_type,) = MANDAT_TYPE_MANDAT(mandat_xml)
        (mandat_type_organe,) = MANDAT_TYPE_ORGANE(mandat_xml)
        (date_debut,) = MANDAT_DATEDEBUT(mandat_xml)
        date_fin = MANDAT_DATEFIN(mandat_xml)
        date_fin = date_fin[0] if len(date_fin) else ""
        mandat_desc = ("{}|{}|{}|[{}|{}]|({})".format(mandat_uid, mandat_type, mandat_type_organe, date_debut, date_fin, organes_desc))
        return mandat_desc

    @staticmethod
    def short_form(mandat_xml):
        return FormatMandat.long_form(mandat_xml)


def format_entity(xml, form_name='default', be_silent_and_return_empty=False):
    try:
        klass = _get_formater_klass_for_fragment(xml)
        form_name += '_form'
        func = getattr(klass, form_name)
    except (ValueError, AttributeError):
        if be_silent_and_return_empty:
            return ""
        else:
            raise
    else:
        return func(xml)


