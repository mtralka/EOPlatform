from typing import cast

from eoplatform.baseClasses import Platform
from eoplatform.download.downloadControl import download
from eoplatform.factory import EOPlatformFactory as factory
from eoplatform.info.infoControl import info


__version__ = "0.1.2"


# for name in factory._find_platform_names():
#     plat = factory.generate_platform(str(name))
#     locals()[cast(Platform, plat).var_name] = plat
