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
from typing import Optional
from typing import Tuple
from typing import Union
from typing import cast

from eoplatform.composites.classes import Composite
from eoplatform.composites.classes import CompositeType
from eoplatform.utils import COMPOSITES_DIR


SEARCH_PATTERN: Final[str] = "**/*.json"


def generate_all_composites() -> Generator[Composite, None, None]:
    for name in find_composite_names():
        platform: Optional[Composite] = generate_composite(str(name))

        if not platform:
            break

        yield platform


@lru_cache(maxsize=5)
def generate_composite(name: str) -> Optional[Composite]:

    target_composite: Path
    for composite in _find_composite_files():
        if composite.stem.upper() == name.upper():
            target_composite = composite
            break
    else:
        return None

    composite_data: Dict[str, Union[str, int]] = _get_composite_data(target_composite)

    return _produce_composite(composite_data)


@lru_cache(maxsize=2)
def find_composite_names() -> List[str]:
    return [f.stem.upper() for f in COMPOSITES_DIR.glob(SEARCH_PATTERN)]


@lru_cache(maxsize=2)
def _find_composite_files() -> List[Path]:
    return [f for f in COMPOSITES_DIR.glob(SEARCH_PATTERN)]


@lru_cache(maxsize=10)
def _get_composite_data(composite_path: Path) -> Dict[str, Union[str, int]]:

    with open(str(composite_path), "r") as file:
        data: Dict[str, Union[str, int]] = json.load(file)

    return data


def _produce_composite(composite_dict: Dict[str, Any]) -> Composite:

    composite_type_str: str = (
        cast(str, composite_dict.pop("type", "NONE")).upper().strip()
    )
    if composite_type_str not in CompositeType.__members__.keys():

        raise ValueError(f"Incorrect composite type {composite_type_str}")
    composite_type: CompositeType = CompositeType[composite_type_str]

    composite_fields: List[Tuple[str, type, Any]] = [
        (
            k,
            cast(type, Any),
            field(),
        )
        for k in composite_dict.keys()
    ]

    composite_docstring: str = f"""{composite_dict.get("name")} ({composite_dict.get("abbreviation")})
        Type: {composite_type.name.capitalize()}

        Formula:
        `{composite_dict.get("formula")}`

        Bands:
        {', '.join(list(cast(List[str],composite_dict.get("bands", []))))}

        
        {composite_dict.get("description")}

        {composite_dict.get("reference")}
        """

    composite_template: type = make_dataclass(
        "Composite",
        composite_fields,
        bases=(Composite,),
        namespace={"__doc__": composite_docstring},
    )

    composite: Composite = composite_template(**composite_dict, type=composite_type)

    return composite
