from tf2_data import EFFECTS, WEARS

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

WEAR_NAMES = [wear for wear in WEARS if not wear.isnumeric()]
EFFECT_NAMES = [
    name
    for name in EFFECTS
    if not name.isnumeric() and name != "Particle 1" and "Attrib_Particle" not in name
]
