"""
Ce module gére le chargemment des fichiers par leurs noms et le cache de ceux-ci dans le répertoire data_src ainsi que la génération des chemins
et noms de fichiers de sortie dans out_dir.

Ces noms data_src et out_dir sont contenus dans deux globales supposées constantes DATA_SRC_REP_NAME et OUT_DIR_REP_NAME

A terme ce module se chargera également du rafraichissement des fichiers dans data_src depuis le site data.assemblee-nationale.fr

"""

import os

SCRIPT_ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_SRC_DIR = os.path.join(SCRIPT_ROOT_DIR, '..', 'data_src')


def get_src_file_path(src_filename, use_sample_files=True):
    """

    :param src_filename: le nom du fichier voulu dans  DATA_SRC_DIR
    :param use_sample_files: permet d'utiliser les fichiers "sample" fournis sans avoir téléchargé les versions les plus récentes des fichiers OpenData AN (utilise pour les tests et expérimentations)
    :return:
    """
    src_filepath = os.path.join(DATA_SRC_DIR, src_filename)
    if not os.path.exists(src_filepath) and use_sample_files:
        basename, ext = os.path.splitext(src_filepath)
        src_filepath = basename + ".sample" + ext
    return src_filepath


def get_out_dir(base_subdir_name=None):
    out_dir_path = os.path.join(SCRIPT_ROOT_DIR, "out_dir", base_subdir_name)
    if not os.path.exists(out_dir_path):
        os.mkdir(out_dir_path)
    return out_dir_path

