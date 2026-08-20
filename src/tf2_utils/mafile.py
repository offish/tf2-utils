import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .decryption import decrypt_data
from .exceptions import EncryptionError


@dataclass
class MaFileData:
    steam_id: str
    username: str
    identity_secret: str
    shared_secret: str


def get_json(file: Path) -> Any:
    return json.loads(file.read_text())


def has_manifest_file(mafile_folder: Path) -> bool:
    for item in mafile_folder.rglob("*"):
        if item.is_file() and item.name == "manifest.json":
            return True

    return False


def is_mafile_unencrypted(mafile: Path) -> bool:
    content = mafile.read_text()
    return "account_name" in content


def get_encryption_values(manifest: Path, mafile: Path) -> dict | None:
    manifest_data = get_json(manifest)

    for entry in manifest_data["entries"]:
        if entry["filename"] == mafile.name:
            return entry


def get_decrypted_data(mafile: Path, code: str | None) -> Any:
    parent_folder = mafile.parent

    if not has_manifest_file(parent_folder):
        raise EncryptionError("maFile is encrypted and no manifest.json was found!")

    if not code:
        raise EncryptionError("No code for maFile decryption was given!")

    manifest_file = parent_folder / "manifest.json"
    encryption_values = get_encryption_values(manifest_file, mafile)

    if not encryption_values:
        raise EncryptionError(f"No encryption values was found for {mafile.name}")

    salt = encryption_values["encryption_salt"]
    iv = encryption_values["encryption_iv"]
    encrypted_data = None

    with open(mafile, "rb") as f:
        encrypted_data = f.read()

    decrypted_text = decrypt_data(code, salt, iv, encrypted_data)

    if not decrypted_text:
        raise EncryptionError(f"Error when trying to decrypt maFile using code {code}")

    return json.loads(decrypted_text)


def get_mafile_data(mafile: Path, code: str | None = None) -> MaFileData:
    content = None

    if is_mafile_unencrypted(mafile):
        content = get_json(mafile)
    else:
        content = get_decrypted_data(mafile, code)

    return MaFileData(
        content["Session"]["SteamID"],
        content["account_name"],
        content["identity_secret"],
        content["shared_secret"],
    )
