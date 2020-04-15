
try:
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources


def get_resource_path(package, file_name):

    with pkg_resources.path(package, file_name) as file_path:
        return file_path
