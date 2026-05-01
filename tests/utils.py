from pathlib import Path


def get_path(file_name: str) -> Path:
    return Path(__file__).parent / "json" / f"{file_name}.json"


def get_overview(keys: int, refs: int, recs: int, scraps: int) -> dict:
    return {
        "Mann Co. Supply Crate Key": keys,
        "Refined Metal": refs,
        "Reclaimed Metal": recs,
        "Scrap Metal": scraps,
    }


tag = [
    {
        "category": "Quality",
        "internal_name": "Unique",
        "localized_category_name": "Quality",
        "localized_tag_name": "Unique",
        "color": "7D6D00",
    }
]

mann_co_supply_crate_key = {
    "market_hash_name": "Mann Co. Supply Crate Key",
    "tags": tag,
}
refined_metal = {"market_hash_name": "Refined Metal", "tags": tag}
reclaimed_metal = {"market_hash_name": "Reclaimed Metal", "tags": tag}
scrap_metal = {"market_hash_name": "Scrap Metal", "tags": tag}

key = [mann_co_supply_crate_key]
ref = [refined_metal]
rec = [reclaimed_metal]
scrap = [scrap_metal]

key_name = ["Mann Co. Supply Crate Key"]
ref_name = ["Refined Metal"]
rec_name = ["Reclaimed Metal"]
scrap_name = ["Scrap Metal"]
