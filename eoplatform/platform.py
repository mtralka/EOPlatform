from eoplatform.factory import EOPlatformFactory as factory


for platform in factory.generate_platform():
    locals()[platform.var_name] = platform
