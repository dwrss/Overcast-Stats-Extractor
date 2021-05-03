from dataclasses import dataclass, field

from overcast_stats_extractor.model.episode import Episode


@dataclass()
class Podcast:
    name: str
    is_subscribed: bool
    _episodes: set[Episode] = field(default_factory=set)
    total_played: int = 0
    total_unplayed: int = 0
    total_started: int = 0
    total_visible: int = 0

    @property
    def episodes(self):
        return self._episodes

    def add(self, episode: Episode):
        self._episodes.add(episode)
        if episode.was_played:
            self.total_played += 1
        else:
            self.total_unplayed += 1
        if not episode.is_deleted:
            self.total_visible += 1
        if episode.is_started:
            self.total_started += 1
