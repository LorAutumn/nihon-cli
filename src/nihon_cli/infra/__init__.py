"""Infrastructure layer for nihon-cli.

This package contains database and other infrastructure-related modules.
"""

from .database import init_db

__all__ = ["init_db"]