import collections
from enum import Enum

Settings = collections.namedtuple(
    "Settings", ["email", "password", "cache_dir", "started_threshold", "cache_override"]
)


class CacheOverride(Enum):
    NORMAL = 1
    FORCE_CACHED = 2
    FORCE_FRESH = 3
