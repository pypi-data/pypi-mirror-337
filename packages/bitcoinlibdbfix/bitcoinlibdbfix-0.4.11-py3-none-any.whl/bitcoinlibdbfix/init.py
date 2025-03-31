from .cli import main
from .version import __version__

__all__ = ['main', '__version__']

# Run pre-install checks when imported during installation
try:
    from .installer import run_pre_install
    run_pre_install()
except ImportError:
    pass
