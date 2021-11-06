import re

chemass_names = re.compile('([A-Z][a-z]?)')
chemass_open = re.compile('(\()')
chemass_num = re.compile('([0-9]+)')
ELEMENT_CLAUSE = re.compile("([A-Z][a-z]?)([0-9]*)")

elements = {
    'H': 1.008,
    'C': 12.01,
    'N': 14.007,
    'O': 16,
    'Na': 22.99,
    'Mg': 24.306,
    'P': 30.974,
    'S': 32.068,
    'Cl': 35.45,
    'K': 39.098,
    'Ca': 40.078,
    'Li': 6.941,
    'Be': 9.012,
    'B': 10.811,
    'F': 18.998,
    'Al': 26.98,
    'Si': 28.086,
    'Ar': 4.003,
    'Fe': 55.845,
    'Cu': 63.546,
    'Ti': 47.867,
    'He': 4,
    'Ne': 20.18,
    'Sc': 44.956,
    'V': 50.942,
    'Cr': 51.996,
    'Mn': 54.938,
    'Co': 58.933,
    'Ni': 58.693,
    'As': 74.922,
    'Br': 79.904,
    'Ag': 107.868,
    'Pt': 195.084,
    'Au': 196.967,
    'Hg': 200.59,
    'Pb': 207.2,
    'Ra': 226.025,
    'U': 238.029
}


def chemass(formula):
    return eval(chemass_formula(formula))


def chemass_formula(formula):
    return chemass_num.sub(r'*\1', chemass_names.sub(r'+elements["\1"]',
                                                     chemass_open.sub(r'+\1', formula)))


def parse_compound(compound):
    assert "(" not in compound, "This parser doesn't grok subclauses"
    return {el: (int(num) if num else 1) for el, num in ELEMENT_CLAUSE.findall(compound)}
