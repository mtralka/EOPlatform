from eoplatform.autoImport import auto_import
from eoplatform.sharedClasses import AutoImport


if auto_import.status == AutoImport.YES:
    from eoplatform.composites.generator import *
