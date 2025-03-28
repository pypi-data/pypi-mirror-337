import functools

def lazy_load(func):
    """Simple decorator for lazy loading attributes"""
    @functools.wraps(func)
    def wrapper(self):
        attr_name = f"_{func.__name__}"
        if not hasattr(self, attr_name) or getattr(self, attr_name) is None:
            setattr(self, attr_name, func(self))
        return getattr(self, attr_name)

    return property(wrapper)



# import os
# import importlib
# import pkgutil
#
# __path__ = [os.path.dirname(__file__)]
#
# for _, module_name, is_pkg in pkgutil.iter_modules(__path__):
#     module = importlib.import_module(f"{__name__}.{module_name}")
#     for attr_name in dir(module):
#         if not attr_name.startswith('_'):
#             globals()[attr_name] = getattr(module, attr_name)
#     globals()[module_name] = module