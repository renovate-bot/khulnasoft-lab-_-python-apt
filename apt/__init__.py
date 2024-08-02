from __future__ import print_function

import apt_pkg

# import some fancy classes
from apt.package import Package as Package, Version as Version
from apt.cache import Cache as Cache, ProblemResolver as ProblemResolver
Cache  # pyflakes
ProblemResolver  # pyflakes
Version  # pyflakes
from apt.cdrom import Cdrom as Cdrom

# init the package system, but do not re-initialize config
if "APT" not in apt_pkg.config:
    apt_pkg.init_config()
apt_pkg.init_system()

__all__ = ['Cache', 'Cdrom', 'Package']
