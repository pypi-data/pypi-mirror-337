#
# MIT License
#
# Copyright (c) 2024-2025 nbiotcloud
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#


"""Read-Only-Memory."""

from functools import cached_property

import ucdp as u
from ucdp_addr.access import RO, Access
from ucdp_glbl.lane import Lane

from .mem import AMemMod
from .memtechconstraints import MemTechConstraints
from .types import MemPwrType


class RomPwrType(MemPwrType):
    """ROM Memory Power Type."""

    def _build(self):
        self._add("pwr", u.EnaType())


class RomMod(AMemMod):
    """Read-Only-Memory."""

    access: u.ClassVar[Access] = RO

    @cached_property
    def memtechconstraints(self) -> MemTechConstraints | None:
        """Memory Technology Constraints."""
        try:
            import ucdpmemtechconfig

            return ucdpmemtechconfig.get_romtechconstraints(self.hiername)
        except (ImportError, AttributeError):
            return None

    def get_pwrlanetype(self, lane: Lane) -> MemPwrType:
        """Determine Power Lane Control Type."""
        return RomPwrType()
