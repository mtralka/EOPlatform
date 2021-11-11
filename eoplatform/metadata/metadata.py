from os import path
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Final
from typing import List
from typing import Optional
from typing import Union
from typing import cast
import xml.etree.ElementTree as ET

from eoplatform.console import console


def _not_found_message(*args: str) -> None:

    console.print(
        f"[red bold encircle]:x:  Did not find:[/][yellow] {','.join(list(args))}"
    )

    return None


def extract_metadata(
    file_path: Union[Path, str], target_attributes: Union[List[str], str], **kwargs: Any
) -> Union[Dict[str, Optional[str]], Dict[str, str]]:
    """Extract metadata from file

    Detects filetype and implements the required metadata extractor. Currently supports
    XML and TXT files. Passes additional kwargs to requisite function

    Parameters
    ----------
    file_path : str
        Full file path to target XML file
    target_attributes: Union[List[str], str]
        List of target attributes desired

    Returns
    -------
    Dict[str, Optional[str]]

    """

    file: Path = Path(file_path) if isinstance(file_path, str) else file_path
    file_extension: Optional[str] = file.suffix

    if not file_extension:
        raise ValueError("Input path does not seem to have a file extension")

    file_extension = file_extension.lower()

    if file_extension == ".xml":
        return extract_XML_metadata(file, target_attributes)
    elif file_extension == ".txt":
        return extract_TXT_metadata(file, target_attributes, **kwargs)
    else:
        raise ValueError(f"{file_extension} not currently supported")


def extract_XML_metadata(
    file_path: Union[str, Path], target_attributes: Union[List[str], str]
) -> Dict[str, str]:
    """Extract metadata from XML file

    Uses ElementTree to extract `target_attributes` from `file_path` XML file.
    Verifies that `file_path` exists and is an XML file. Returns dictionary of
    all found attributes

    Parameters
    ----------
    file_path : Union[Path, str]
        Full file path to target XML file
    target_attributes: Union[List[str], str]
        List of target attributes desired

    Returns
    -------
    Dict[str, str]

    """

    X_PATH_WILDCARD: Final[str] = ".//"

    file: Path = Path(file_path) if isinstance(file_path, str) else file_path
    target_attributes_list: List[str] = (
        [target_attributes] if isinstance(target_attributes, str) else target_attributes
    )

    if not file.exists():
        raise FileNotFoundError(f"{file} does not exist")

    file_extension = file.suffix

    if not file_extension:
        raise ValueError("File must have a `.xml` file extension")
    if file_extension.lower() != ".xml":
        raise TypeError(f"{file_path} is not an XML file")

    namespaces: Dict[str, str] = dict(
        [node for _, node in ET.iterparse(file_path, events=["start-ns"])]
    )

    tree: ET.ElementTree = ET.parse(file_path)
    found_attributes: Dict[str, str] = {}

    for target_attribute in target_attributes_list:

        target_el: Optional[ET.Element] = tree.find(
            X_PATH_WILDCARD + target_attribute, namespaces=namespaces
        )

        if target_el is None:
            _not_found_message(target_attribute)
            continue

        found_attributes[target_attribute] = cast(str, target_el.text)

    return found_attributes


def extract_TXT_metadata(
    file_path: Union[Path, str],
    target_attributes: Union[List[str], str],
    delineator: str = "=",
) -> Dict[str, Optional[str]]:
    """Extract metadata from TXT file

    Extracts `target_attributes` from `file_path` TXT file. Assumes metadata
    keys and values are seperated by `delineator`
    Verifies that `file_path` exists and is an TXT file. Returns dictionary of
    all found attributes

    Parameters
    ----------
    file_path : Union[Path, str]
        Full file path to target TXT file
    target_attributes: Union[List[str], str]
        List of target attributes desired

    Returns
    -------
    Dict[str, str]

    """

    file: Path = Path(file_path) if isinstance(file_path, str) else file_path
    target_attributes_list: List[str] = (
        [target_attributes] if isinstance(target_attributes, str) else target_attributes
    )

    if not file.exists():
        raise FileNotFoundError(f"{file_path} does not exist")

    file_extension = file.suffix

    if not file_extension:
        raise ValueError("File must have a `.txt` file extension")
    if file_extension.lower() != ".txt":
        raise TypeError(f"{file_path} is not a TXT file")

    found_attributes: Dict[str, Optional[str]] = {
        k: None for k in target_attributes_list
    }

    with file.open() as f:
        for line_number, line in enumerate(f):

            split: List[str] = line.split(delineator)
            split = [x.strip(" ") for x in split]

            if not len(split) <= 2:
                raise AssertionError(
                    f"Line {line_number} violates formatting assumptions"
                )

            if split[0] not in target_attributes_list:
                continue

            if len(split) != 2:
                raise AssertionError(
                    f"Found {split[0]} on line {line_number} but line does not meet format assumptions"
                )

            found_attributes[split[0]] = split[1].strip("\n")

    if not all(found_attributes.values()):
        not_found: List[str] = list(
            set(target_attributes_list)
            - set(k for k, v in found_attributes.items() if v is not None)
        )
        _not_found_message(*not_found)

    return found_attributes
