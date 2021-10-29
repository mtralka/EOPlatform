from dataclasses import field
from dataclasses import make_dataclass
import json
from pathlib import Path
import sys
from typing import Any
from typing import Dict
from typing import Generator
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union
from typing import cast

from eoplatform.composites.baseClasses import Composite
from eoplatform.composites.baseClasses import CompositeType
from eoplatform.utils import COMPOSITES_DIR


if sys.version_info >= (3, 8, 0):
    from typing import Final  # type: ignore
else:
    from typing_extensions import Final


class EOCompositeFactory:
    """On-demand composite factory"""

    @staticmethod
    def generate_all_composites() -> Generator[Composite, None, None]:
        for name in EOCompositeFactory.find_composite_names():
            platform: Optional[Composite] = EOCompositeFactory.generate_composite(
                str(name)
            )

            if not platform:
                break

            yield platform

    @staticmethod
    def generate_composite(name: str) -> Optional[Composite]:

        target_composite: Path
        for composite in EOCompositeFactory._find_composite_files():
            if composite.stem.upper() == name.upper():
                target_composite = composite
                break
        else:
            return None

        composite_data: Dict[
            str, Union[str, int]
        ] = EOCompositeFactory._get_composite_data(target_composite)

        return EOCompositeFactory._produce_composite(composite_data)

    @staticmethod
    def find_composite_names() -> List[str]:
        PATTERN: Final[str] = "**/*.json"
        return [f.stem for f in COMPOSITES_DIR.glob(PATTERN)]

    @staticmethod
    def _find_composite_files() -> Generator[Path, None, None]:
        PATTERN: Final[str] = "**/*.json"
        return cast(Generator[Path, None, None], COMPOSITES_DIR.glob(PATTERN))

    @staticmethod
    def _get_composite_data(composite_path: Path) -> Dict[str, Union[str, int]]:

        with open(str(composite_path), "r") as file:
            data: Dict[str, Union[str, int]] = json.load(file)

        return data

    @staticmethod
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
