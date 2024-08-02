from __future__ import print_function

from typing import Optional
import glob

import apt_pkg
from apt.progress.base import CdromProgress


class Cdrom(apt_pkg.Cdrom):
    """Support for apt-cdrom like features.

    This class has several optional parameters for initialisation, which may
    be used to influence the behaviour of the object:

    The optional parameter `progress` is a CdromProgress() subclass, which will
    ask for the correct cdrom, etc. If not specified or None, a CdromProgress()
    object will be used.

    The optional parameter `mountpoint` may be used to specify an alternative
    mountpoint.

    If the optional parameter `nomount` is True, the cdroms will not be
    mounted. This is the default behaviour.
    """

    def __init__(self, progress=None, mountpoint=None, nomount=True):
        # type: (Optional[CdromProgress], Optional[str], bool) -> None
        apt_pkg.Cdrom.__init__(self)
        if progress is None:
            self._progress = CdromProgress()
        else:
            self._progress = progress
        # see if we have a alternative mountpoint
        if mountpoint is not None:
            apt_pkg.config.set("Acquire::cdrom::mount", mountpoint)
        # do not mess with mount points by default
        if nomount:
            apt_pkg.config.set("APT::CDROM::NoMount", "true")
        else:
            apt_pkg.config.set("APT::CDROM::NoMount", "false")

    def add(self, progress=None):
        # type: (Optional[CdromProgress]) -> bool
        """Add cdrom to the sources.list."""
        return apt_pkg.Cdrom.add(self, progress or self._progress)

    def ident(self, progress=None):
        # type: (Optional[CdromProgress]) -> str
        """Identify the cdrom."""
        return apt_pkg.Cdrom.ident(self, progress or self._progress)

    @property
    def in_sources_list(self):
        # type: () -> bool
        """Check if the cdrom is already in the current sources.list."""
        cd_id = self.ident()
        if cd_id is None:
            # FIXME: throw exception instead
            return False
        # Get a list of files
        src = glob.glob(apt_pkg.config.find_dir("Dir::Etc::sourceparts") + '*')
        src.append(apt_pkg.config.find_file("Dir::Etc::sourcelist"))
        # Check each file
        for fname in src:
            with open(fname) as fobj:
                for line in fobj:
                    if not line.lstrip().startswith("#") and cd_id in line:
                        return True
        return False
