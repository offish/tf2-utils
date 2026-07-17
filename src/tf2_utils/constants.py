from tf2_data import EFFECTS

KEY = "Mann Co. Supply Crate Key"
REF = "Refined Metal"
REC = "Reclaimed Metal"
SCRAP = "Scrap Metal"

QUALITY_NAMES = [
    "Genuine",
    "Vintage",
    "Unusual",
    "Unique",
    "Strange",
    "Haunted",
    "Collector's",
    "Decorated Weapon",
]

EFFECT_NAMES = [
    name
    for name in EFFECTS.keys()
    if not name.isnumeric() and name != "Particle 1" and "Attrib_Particle" not in name
]
