from host_info.utils.importutils import get_platform_module

platform_module = get_platform_module(__name__)

get_platform_info = platform_module.get_platform_info
