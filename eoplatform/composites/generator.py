from eoplatform.autoImport import auto_import
from eoplatform.composites.factory import EOCompositeFactory as factory
from eoplatform.sharedClasses import AutoImport


if auto_import.status == AutoImport.YES:
    for composite in factory.generate_all_composites():
        locals()[composite.abbreviation] = composite
