import sys


if sys.version_info >= (3, 8, 0):
    from typing import Final  # type: ignore
else:
    from typing_extensions import Final

from os import path
from typing import Dict
from typing import List
from typing import Optional
from typing import cast
import xml.etree.ElementTree as ET

from eoplatform.console import console


def _not_found_message(*args: str) -> None:

    console.print(
        f"[red bold encircle]:x:  Did not find:[/][yellow] {','.join(list(args))}"
    )

    return None


def extract_XML_metadata(
    file_path: str, target_attributes: List[str]
) -> Dict[str, str]:
    """Extract metadata from XML file

    Uses ElementTree to extract `target_attributes` from `file_path` XML file.
    Verifies that `file_path` exists and is an XML file. Returns dictionary of
    all found attributes

    Parameters
    ----------
    file_path : str
        Full file path to target XML file
    target_attributes: List[str]
        List of target attributes desired

    Returns
    -------
    Dict[str, str]

    """

    X_PATH_WILDCARD: str = ".//"

    if not path.exists(file_path):
        raise FileNotFoundError(f"{file_path} does not exist")

    _, file_extension = path.splitext(file_path)
    if file_extension != ".xml":
        raise TypeError(f"{file_path} is not an XML file")

    namespaces: Dict[str, str] = dict(
        [node for _, node in ET.iterparse(file_path, events=["start-ns"])]
    )

    tree: ET.ElementTree = ET.parse(file_path)
    found_attributes: Dict[str, str] = {}

    for target_attribute in target_attributes:

        target_el: Optional[ET.Element] = tree.find(
            X_PATH_WILDCARD + target_attribute, namespaces=namespaces
        )

        if target_el is None:
            _not_found_message(target_attribute)
            continue

        found_attributes[target_attribute] = cast(str, target_el.text)

    return found_attributes


def extract_TXT_metadata(
    file_path: str, target_attributes: List[str], delineator: str = "="
) -> Dict[str, Optional[str]]:
    """Extract metadata from TXT file

    Extracts `target_attributes` from `file_path` TXT file. Assumes metadata
    keys and values are seperated by `delineator`
    Verifies that `file_path` exists and is an TXT file. Returns dictionary of
    all found attributes

    Parameters
    ----------
    file_path : str
        Full file path to target TXT file
    target_attributes: List[str]
        List of target attributes desired

    Returns
    -------
    Dict[str, str]

    """

    if not path.exists(file_path):
        raise FileNotFoundError(f"{file_path} does not exist")

    _, file_extension = path.splitext(file_path)
    if file_extension != ".txt":
        raise TypeError(f"{file_path} is not a TXT file")

    found_attributes: Dict[str, Optional[str]] = {k: None for k in target_attributes}

    with open(file_path) as file:
        for line_number, line in enumerate(file):

            split: List[str] = line.split("=")
            split = [x.strip(" ") for x in split]

            if not len(split) <= 2:
                raise AssertionError(
                    f"Line {line_number} violates formatting assumptions"
                )

            if split[0] not in target_attributes:
                continue

            if len(split) != 2:
                raise AssertionError(
                    f"Found {split[0]} on line {line_number} but line does not meet format assumptions"
                )

            found_attributes[split[0]] = split[1].strip("\n")

    if not all(found_attributes.values()):
        not_found: List[str] = list(
            set(target_attributes)
            - set(k for k, v in found_attributes.items() if v is not None)
        )
        _not_found_message(*not_found)

    return found_attributes