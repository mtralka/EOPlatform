from eoplatform.sharedClasses import AutoImport
from eoplatform.autoImport import auto_import


if auto_import.status == AutoImport.YES:
    from eoplatform.platforms.generator import *
