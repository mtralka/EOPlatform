from eoplatform.autoImport import auto_import
from eoplatform.platforms.factory import EOPlatformFactory as factory
from eoplatform.sharedClasses import AutoImport


if auto_import.status == AutoImport.YES:
    for platform in factory.generate_all_platforms():
        locals()[platform.var_name] = platform
