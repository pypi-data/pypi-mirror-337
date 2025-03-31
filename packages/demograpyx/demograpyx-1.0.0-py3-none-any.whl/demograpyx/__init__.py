from sys import version_info

if version_info < (3, 10, 0):
    raise RuntimeError("demograpyx requires Python 3.10 or newer to work.")

from typing import NamedTuple

from .clients import Genderize, Agify, Nationalize
from .objects import CountryCode, GenderPrediction, AgePrediction, NationalityPrediction, CountryPrediction

__all__ = ("__version__", "Genderize", "Agify", "Nationalize", "CountryCode", "GenderPrediction", "AgePrediction", "NationalityPrediction", "CountryPrediction")

class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int

__version__ = VersionInfo(major=1, minor=0, micro=0)

del NamedTuple, version_info