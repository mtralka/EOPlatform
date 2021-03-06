from dataclasses import dataclass
from dataclasses import field
from dataclasses import make_dataclass
from functools import lru_cache
import json
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Final
from typing import Generator
from typing import List
from typing import Mapping
from typing import Optional
from typing import Tuple
from typing import Union
from typing import cast

from eoplatform.platforms.classes import Band
from eoplatform.platforms.classes import Bands
from eoplatform.platforms.classes import Platform
from eoplatform.utils import PLATFORMS_DIR


SEARCH_PATTERN: Final[str] = "**/*.json"


@dataclass
class PlatformNode:
    key: str
    value: Union[str, int, float, Dict[str, Any]]
    meta: Optional[Dict[str, Any]]


def generate_all_platforms() -> Generator[Platform, None, None]:
    for name in find_platform_names():
        platform: Optional[Platform] = generate_platform(str(name))

        if not platform:
            break

        yield platform


@lru_cache(maxsize=5)
def generate_platform(name: str) -> Optional[Platform]:

    target_platform: Path
    for platform in _find_platform_files():
        if platform.stem.upper() == name.upper():
            target_platform = platform
            break
    else:
        return None

    platform_data: Dict[str, Union[str, int]] = _get_platform_data(target_platform)

    return _produce_platform(platform_data)


@lru_cache(maxsize=2)
def _find_platform_files() -> List[Path]:

    return [f for f in PLATFORMS_DIR.glob(SEARCH_PATTERN)]


@lru_cache(maxsize=2)
def find_platform_names() -> List[str]:

    return [f.stem.upper() for f in PLATFORMS_DIR.glob(SEARCH_PATTERN)]


@lru_cache(maxsize=10)
def _get_platform_data(platform_path: Path) -> Dict[str, Union[str, int]]:

    with open(str(platform_path), "r") as file:
        data: Dict[str, Union[str, int]] = json.load(file)

    return data


def _produce_platform(platform_dict: Dict[str, Any]) -> Platform:

    platform_bands = platform_dict.pop("bands")

    platform_nodes: List[PlatformNode] = [
        PlatformNode(
            key=k,
            value=v.get("value", v) if isinstance(v, dict) else v,
            meta=v.get("meta", {}) if isinstance(v, dict) else {},
        )
        for k, v in platform_dict.items()
    ]

    platform_fields: List[Tuple[str, type, Any]] = [
        (
            n.key,
            cast(type, Any),
            field(default=n.value, metadata={**cast(Mapping[str, Any], n.meta)}),
        )
        for n in platform_nodes
    ]

    if platform_bands:
        bands_template: type = make_dataclass(
            "Bands",
            [
                (b["abbreviation"], Band, field(default=cast(Any, Band(**b))))
                for b in platform_bands
            ],
            bases=(Bands,),
        )
        platform_fields.append(("bands", Bands, field(default=bands_template())))

    platform_template: type = make_dataclass(
        "Platforms", platform_fields, bases=(Platform,)
    )

    platform: Platform = platform_template()

    return platform
