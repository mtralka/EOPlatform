from importlib import resources
import json
from pathlib import Path
import sys
from typing import Any
from typing import Dict
from typing import Generator
from typing import Iterator
from typing import List
from typing import Union

from eoplatform.baseClasses import Platform


if sys.version_info >= (3, 8, 0):
    from typing import Final  # type: ignore
else:
    from typing_extensions import Final

PLATFORM_PATH: Final[str] = "eoplatform.platforms"


class EOPlatformFactory:
    @staticmethod
    def generate_platform() -> Generator[Platform, None, None]:

        platform_names: List[str] = EOPlatformFactory._find_platform_files()

        for name in platform_names:
            platform_data: Dict[
                str, Union[str, int]
            ] = EOPlatformFactory._get_platform_data(name)
            yield EOPlatformFactory._produce_platform(platform_data)

    @staticmethod
    def _find_platform_files() -> List[str]:
        directory: Iterator[str] = resources.contents(PLATFORM_PATH)
        test: List[str] = [f for f in directory if f[-5:] == ".json"]

        return test

    @staticmethod
    def _get_platform_data(platform_name: str) -> Dict[str, Union[str, int]]:

        with resources.open_text(PLATFORM_PATH, platform_name) as file:
            data: Dict[str, Union[str, int]] = json.load(file)

        return data

    @staticmethod
    def _produce_platform(platform_dict: Dict[str, Any]) -> Platform:
        return Platform(**platform_dict)
