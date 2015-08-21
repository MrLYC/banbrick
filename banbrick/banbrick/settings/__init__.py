for setting_name in ("prod", "dev", "demo"):
    if setting_name == "prod":
        try:
            from .prod import *
            break
        except ImportError:
            pass
    elif setting_name == "dev":
        try:
            from .dev import *
            break
        except ImportError:
            pass
    elif setting_name == "demo":
        try:
            from .demo import *
            break
        except ImportError:
            pass
