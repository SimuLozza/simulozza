import pathlib


ME = pathlib.Path(__file__)


def data_file(filename):
    return str(ME.parents[1] / 'data' / filename)


def level_names():
    names = sorted((ME.parents[1] / 'data').glob('level?-?.tmx'))
    return names
