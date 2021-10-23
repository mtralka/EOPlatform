from eoplatform.factory import EOPlatformFactory as eop


for platform in eop.generate_platform():
    locals()[platform.var_name] = platform
