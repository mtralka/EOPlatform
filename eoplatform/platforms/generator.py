from eoplatform.auto_import import auto_import
from eoplatform.platforms.factory import generate_all_platforms
from eoplatform.shared_classes import AutoImport


if auto_import.status == AutoImport.YES:
    for platform in generate_all_platforms():
        locals()[platform.var_name] = platform
