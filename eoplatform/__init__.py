from typing import cast

from eoplatform.baseClasses import Platform
from eoplatform.download.downloadControl import download
from eoplatform.factory import EOPlatformFactory as factory
from eoplatform.info.infoControl import info


__version__ = "0.2.0"

for platform in factory.generate_all_platforms():
    locals()[platform.var_name] = platform
