# Define a dictionary to map element groups to colors
element_colors = {
    "Alkali Metals": "red",
    "Alkaline Earth Metals": "orange",
    "Transition Metals": "grey",
    "Lanthanides": "blue",
    "Actinides": "brown",
    "Metalloids": "purple",
    "Halogens": "green",
    "Noble Gases": "gray",
    "Post-transition Metals": "olive",
}


# Define a function to classify elements into groups
def classify_element(element):
    if element in ["Li", "Na", "K", "Rb", "Cs", "Fr"]:
        return "Alkali Metals"
    elif element in ["Be", "Mg", "Ca", "Sr", "Ba", "Ra"]:
        return "Alkaline Earth Metals"
    elif element in [
        "Sc",
        "Ti",
        "V",
        "Cr",
        "Mn",
        "Fe",
        "Co",
        "Ni",
        "Cu",
        "Zn",
        "Y",
        "Zr",
        "Nb",
        "Mo",
        "Tc",
        "Ru",
        "Rh",
        "Pd",
        "Ag",
        "Cd",
        "Hf",
        "Ta",
        "W",
        "Re",
        "Os",
        "Ir",
        "Pt",
        "Au",
        "Hg",
    ]:
        return "Transition Metals"
    elif element in [
        "La",
        "Ce",
        "Pr",
        "Nd",
        "Pm",
        "Sm",
        "Eu",
        "Gd",
        "Tb",
        "Dy",
        "Ho",
        "Er",
        "Tm",
        "Yb",
        "Lu",
    ]:
        return "Lanthanides"
    elif element in [
        "Ac",
        "Th",
        "Pa",
        "U",
        "Np",
        "Pu",
        "Am",
        "Cm",
        "Bk",
        "Cf",
        "Es",
        "Fm",
        "Md",
        "No",
        "Lr",
    ]:
        return "Actinides"
    elif element in ["B", "Si", "Ge", "As", "Sb", "Te", "Po", "At"]:
        return "Metalloids"
    elif element in ["F", "Cl", "Br", "At", "In"]:
        return "Halogens"
    elif element in ["He", "Ne", "Ar", "Kr", "Xe", "Rn"]:
        return "Noble Gases"
    elif element in [
        "Al",
        "Ga",
        "In",
        "Tl",
        "Pb",
        "Bi",
        "Nh",
        "Fl",
        "Mc",
        "Lv",
        "Ts",
        "Og",
    ]:
        return "Post-transition Metals"
    else:
        return "Other"
