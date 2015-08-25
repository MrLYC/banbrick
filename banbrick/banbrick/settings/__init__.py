from ycyc.base.funcutils import export_module
from ycyc.base.txtutils import sep_join

for setting_name in ("prod", "dev", "demo"):
    try:
        export_module(sep_join(".", [__name__, setting_name]))
        break
    except ImportError:
        pass
