from tf2_data import EFFECTS, QUALITIES

__all__ = [
    "has_festivized_in_name",
    "has_uncraftable_in_name",
    "has_non_craftable_in_name",
    "is_craftable",
    "has_australium_in_name",
    "has_strange_in_name",
    "has_basic_killstreak_in_name",
    "has_specialized_killstreak_in_name",
    "has_professional_killstreak_in_name",
    "has_killstreak_in_name",
    "get_effect_in_name",
    "get_quality_from_name",
]

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

EFFECT_NAMES = [i for i in EFFECTS.keys() if not i.isnumeric()]


def has_festivized_in_name(name: str) -> bool:
    return "Festivized " in name


def has_uncraftable_in_name(name: str) -> bool:
    return "Uncraftable " in name


def has_non_craftable_in_name(name: str) -> bool:
    return "Non-Craftable " in name


def is_craftable(name: str) -> bool:
    return not (has_uncraftable_in_name(name) or has_non_craftable_in_name(name))


def has_australium_in_name(name: str) -> bool:
    return "Australium " in name


def has_strange_in_name(name: str) -> bool:
    return "Strange " in name


def has_basic_killstreak_in_name(name: str) -> bool:
    return name.startswith("Basic Killstreak ")


def has_specialized_killstreak_in_name(name: str) -> bool:
    return name.startswith("Specialized ")


def has_professional_killstreak_in_name(name: str) -> bool:
    return name.startswith("Professional ")


def has_killstreak_in_name(name: str) -> bool:
    return (
        has_basic_killstreak_in_name(name)
        or has_specialized_killstreak_in_name(name)
        or has_professional_killstreak_in_name(name)
    )


def get_effect_in_name(name: str) -> int:
    for effect in EFFECT_NAMES:
        if effect in name:
            return EFFECTS[effect]

    return -1


def get_quality_from_name(name: str) -> int:
    quality = 6

    for part in name.split(" "):
        if part not in QUALITY_NAMES:
            continue

        quality = QUALITIES[part]
        break

    return quality
