import base64
import hashlib
import os
import zipfile

NAME, VERSION = "gcl_dep", "0.1.0"


def _record(entries):
    lines = []
    for name, data in entries:
        digest = base64.urlsafe_b64encode(hashlib.sha256(data).digest()).rstrip(b"=").decode()
        lines.append(f"{name},sha256={digest},{len(data)}")
    return "\n".join(lines)


def get_requires_for_build_wheel(config_settings=None):
    return []


def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    name = f"{NAME}-{VERSION}-py3-none-any.whl"
    dist = f"{NAME}-{VERSION}.dist-info"
    with open(os.path.join(os.path.dirname(__file__), "gcl_dep.py"), "rb") as stream:
        module = stream.read()
    entries = [
        ("gcl_dep.py", module),
        (f"{dist}/METADATA", f"Metadata-Version: 2.1\nName: gcl-dep\nVersion: {VERSION}\n".encode()),
        (f"{dist}/WHEEL", b"Wheel-Version: 1.0\nGenerator: gcl\nRoot-Is-Purelib: true\nTag: py3-none-any\n"),
    ]
    record = _record(entries) + f"\n{dist}/RECORD,,\n"
    with zipfile.ZipFile(os.path.join(wheel_directory, name), "w", zipfile.ZIP_DEFLATED) as archive:
        for entry, data in entries:
            archive.writestr(entry, data)
        archive.writestr(f"{dist}/RECORD", record)
    return name
