from importlib import resources
import json
from os import stat
from pathlib import Path
import sys
from typing import Any
from typing import Dict
from typing import Generator
from typing import Iterator
from typing import List
from typing import Optional
from typing import Union
from typing import cast

from eoplatform.baseClasses import Platform
from eoplatform.utils import PLATFORMS_DIR


if sys.version_info >= (3, 8, 0):
    from typing import Final  # type: ignore
else:
    from typing_extensions import Final


# ON DEMAND
# PLATFORM_PATH: Final[str] = "eoplatform.platforms"

# class EOPlatformFactory:
#     @staticmethod
#     def generate_platform(name: str) -> Optional[Platform]:

#         if name not in EOPlatformFactory._get_platform_names():
#             return None

#         platform_data: Dict[
#             str, Union[str, int]
#         ] = EOPlatformFactory._get_platform_data(name)

#         return EOPlatformFactory._produce_platform(platform_data)

#     @staticmethod
#     def _get_platform_names() -> List[str]:
#         PATTERN: Final[str] = "**/*.json"
#         return [f.stem for f in PLATFORMS_DIR.glob(PATTERN)]

#     @staticmethod
#     def _get_platform_data(platform_name: str) -> Dict[str, Union[str, int]]:

#         with resources.open_text(PLATFORM_PATH, platform_name + ".json") as file:
#             data: Dict[str, Union[str, int]] = json.load(file)

#         return data

# @staticmethod
# def _find_platform_names() -> Generator[Path, None, None]:
#     PATTERN: Final[str] = "**/*.json"
#     return PLATFORMS_DIR.glob(PATTERN)

# @staticmethod
# def _produce_platform(platform_dict: Dict[str, Any]) -> Platform:
#     return Platform(**platform_dict)


class EOPlatformFactory:
    @staticmethod
    def generate_platform() -> Generator[Platform, None, None]:

        platform_paths: Generator[
            Path, None, None
        ] = EOPlatformFactory._find_platform_files()
        for name in platform_paths:
            platform_data: Dict[
                str, Union[str, int]
            ] = EOPlatformFactory._get_platform_data(name)
            yield EOPlatformFactory._produce_platform(platform_data)

    @staticmethod
    def _find_platform_files() -> Generator[Path, None, None]:
        PATTERN: Final[str] = "**/*.json"
        return cast(Generator[Path, None, None], PLATFORMS_DIR.glob(PATTERN))

    @staticmethod
    def _get_platform_data(platform_file: Path) -> Dict[str, Union[str, int]]:
        with open(platform_file, "r") as file:
            data: Dict[str, Union[str, int]] = json.load(file)
        return data

    @staticmethod
    def _produce_platform(platform_dict: Dict[str, Any]) -> Platform:
        return Platform(**platform_dict)

    # @staticmethod
    # def _get_platform_names() -> List[str]:
    #     PATTERN: Final[str] = "**/*.json"
    #     return [f.stem for f in PLATFORMS_DIR.glob(PATTERN)]
