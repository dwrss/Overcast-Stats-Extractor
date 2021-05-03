from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Episode:
    title: str
    is_deleted: bool
    is_started: bool
    was_played: bool
    last_modified: datetime
