from tf2_data import EFFECTS, QUALITIES

from .constants import EFFECT_NAMES, QUALITY_NAMES


def has_festivized_in_name(name: str) -> bool:
    return "Festivized " in name


def has_uncraftable_in_name(name: str) -> bool:
    return "Uncraftable " in name


def has_non_craftable_in_name(name: str) -> bool:
    return "Non-Craftable " in name


def is_craftable(name: str) -> bool:
    return not (has_uncraftable_in_name(name) or has_non_craftable_in_name(name))


def has_australium_in_name(name: str) -> bool:
    return "Australium " in name and "Australium Gold" not in name


def has_strange_in_name(name: str) -> bool:
    return "Strange " in name and "Strange Part: " not in name


def has_killstreak_in_name(name: str) -> bool:
    return "Killstreak " in name


def has_specialized_killstreak_in_name(name: str) -> bool:
    return "Specialized Killstreak " in name


def has_professional_killstreak_in_name(name: str) -> bool:
    return "Professional Killstreak " in name


def is_killstreak(name: str) -> bool:
    return has_killstreak_in_name(name)


def get_effect_in_name(name: str) -> int:
    for effect in EFFECT_NAMES:
        if effect in name:
            return EFFECTS[effect]

    return -1


def get_quality_from_name(name: str) -> int:
    quality = 6

    if "Strange Part: " in name:
        return quality

    for part in name.split(" "):
        if part not in QUALITY_NAMES:
            continue

        quality = QUALITIES[part]
        break

    return quality
