from eoplatform.auto_import import auto_import
from eoplatform.composites.factory import generate_all_composites
from eoplatform.shared_classes import AutoImport


if auto_import.status == AutoImport.YES:
    for composite in generate_all_composites():
        locals()[composite.abbreviation] = composite
