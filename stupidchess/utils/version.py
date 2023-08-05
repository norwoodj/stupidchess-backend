import json
import os.path
from .. import LOGGER

VERSION_FILE_NAME = "version.json"
MISSING_VERSION_FIELD = "UNSPECIFIED"


def load_version_info(package_root):
    version_file = os.path.join(package_root, VERSION_FILE_NAME)

    try:
        with open(version_file) as f:
            version_info = json.load(f)
            LOGGER.info(
                f"Started stupidchess server version {version_info.get('version', MISSING_VERSION_FIELD)}"
            )
            return version_info
    except Exception as e:
        LOGGER.warn(f"Failed to load version file: {e}")
        return {
            "build_timestamp": MISSING_VERSION_FIELD,
            "git_revision": MISSING_VERSION_FIELD,
            "version": MISSING_VERSION_FIELD,
        }
