import json
from os import stat
from pathlib import Path
import sys
from typing import Any
from typing import Dict
from typing import Generator
from typing import Union

from eoplatform.baseClasses import Platform


# if sys.version_info >= (3, 8, 0):
#     from typing import Final  # type: ignore
# else:
#     from typing_extensions import Final

PLATFORM_PATH: Path = Path("eoplatform/platforms")


class EOPlatformFactory:
    @staticmethod
    def generate_platform() -> Generator[Platform, None, None]:

        platform_paths: Generator[
            Path, None, None
        ] = EOPlatformFactory._find_platform_files()

        for file in platform_paths:
            platform_data: Dict[
                str, Union[str, int]
            ] = EOPlatformFactory._get_platform_data(file)
            yield EOPlatformFactory._produce_platform(platform_data)

    @staticmethod
    def _find_platform_files() -> Generator[Path, None, None]:
        pattern: str = "*.json"
        return Path(PLATFORM_PATH).glob(pattern)

    @staticmethod
    def _get_platform_data(platform_file: Path) -> Dict[str, Union[str, int]]:
        with open(platform_file, "r") as file:
            data: Dict[str, Union[str, int]] = json.load(file)
        return data

    @staticmethod
    def _produce_platform(platform_dict: Dict[str, Any]) -> Platform:
        return Platform(**platform_dict)
