from eoplatform.auto_import import auto_import
from eoplatform.shared_classes import AutoImport


if auto_import.status == AutoImport.YES:
    from eoplatform.composites.generator import *
