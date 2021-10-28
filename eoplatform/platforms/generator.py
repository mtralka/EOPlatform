from eoplatform.platforms.factory import EOPlatformFactory as factory


for platform in factory.generate_all_platforms():
    locals()[platform.var_name] = platform
