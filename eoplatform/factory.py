from dataclasses import dataclass
from dataclasses import field
from dataclasses import make_dataclass
import json
from pathlib import Path
import sys
from typing import Any
from typing import Dict
from typing import Generator
from typing import List
from typing import Mapping
from typing import Optional
from typing import Tuple
from typing import Union
from typing import cast

from eoplatform.baseClasses import Band
from eoplatform.baseClasses import Bands
from eoplatform.baseClasses import Platform
from eoplatform.utils import PLATFORMS_DIR


if sys.version_info >= (3, 8, 0):
    from typing import Final  # type: ignore
else:
    from typing_extensions import Final

PLATFORM_PATH: Final[str] = "eoplatform.platforms"


@dataclass
class PlatformNode:
    key: str
    value: Union[str, int, float, Dict[str, Any]]
    meta: Optional[Dict[str, Any]]


class EOPlatformFactory:
    """On-demand platform factory"""

    @staticmethod
    def generate_all_platforms() -> Generator[Platform, None, None]:
        for name in EOPlatformFactory._find_platform_names():
            platform: Optional[Platform] = EOPlatformFactory.generate_platform(
                str(name)
            )

            if not platform:
                break

            yield platform

    @staticmethod
    def generate_platform(name: str) -> Optional[Platform]:

        target_platform: Path
        for platform in EOPlatformFactory._find_platform_files():
            if platform.stem == name:
                target_platform = platform
                break
        else:
            return None

        platform_data: Dict[
            str, Union[str, int]
        ] = EOPlatformFactory._get_platform_data(target_platform)

        return EOPlatformFactory._produce_platform(platform_data)

    @staticmethod
    def _find_platform_files() -> Generator[Path, None, None]:
        PATTERN: Final[str] = "**/*.json"
        return cast(Generator[Path, None, None], PLATFORMS_DIR.glob(PATTERN))

    @staticmethod
    def _find_platform_names() -> List[str]:
        PATTERN: Final[str] = "**/*.json"
        return [f.stem for f in PLATFORMS_DIR.glob(PATTERN)]

    @staticmethod
    def _get_platform_data(platform_path: Path) -> Dict[str, Union[str, int]]:

        with open(str(platform_path), "r") as file:
            data: Dict[str, Union[str, int]] = json.load(file)

        return data

    @staticmethod
    def _produce_platform(platform_dict: Dict[str, Any]) -> Platform:

        platform_bands = platform_dict.pop("bands")

        platform_nodes: Dict[str, PlatformNode] = {
            k: PlatformNode(
                key=k,
                value=v.get("value", v) if isinstance(v, dict) else v,
                meta=v.get("meta", {}) if isinstance(v, dict) else {},
            )
            for k, v in platform_dict.items()
        }

        bands_template: type = make_dataclass(
            "Bands",
            [
                (b["abbreviation"], Band, field(default=cast(Any, Band(**b))))
                for b in platform_bands
            ],
            bases=(Bands,),
        )

        platform_fields: List[Tuple[str, type, Any]] = [
            (
                n.key,
                cast(type, Any),
                field(default=n.value, metadata={**cast(Mapping[str, Any], n.meta)}),
            )
            for n in platform_nodes.values()
        ]
        platform_fields.append(("bands", Bands, field(default=bands_template())))

        platform_template: type = make_dataclass(
            "Platforms", platform_fields, bases=(Platform,)
        )

        platform: Platform = platform_template()

        return platform
