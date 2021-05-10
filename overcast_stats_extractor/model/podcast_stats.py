import collections
from dataclasses import dataclass, field
from typing import Optional

from overcast_stats_extractor.model.podcast import Podcast

Totals = collections.namedtuple("Totals", ["podcasts", "episodes"])
PodcastTotals = collections.namedtuple("PodcastTotals", ["total", "subscribed"])
EpisodeTotals = collections.namedtuple(
    "EpisodeTotals", ["total", "played", "not_played", "started", "visible"]
)


@dataclass
class PodcastStats:
    _podcasts: [Podcast] = field(default_factory=list)
    _podcast_totals = PodcastTotals(total=0, subscribed=0)
    _episode_totals = EpisodeTotals(
        total=0, played=0, not_played=0, started=0, visible=0
    )
    _podcast_least_played_episodes: Optional[Podcast] = None
    _podcast_most_played_episodes: Optional[Podcast] = None

    def add(self, podcast: Podcast):
        self._podcasts.append(podcast)
        self._podcast_totals = PodcastTotals(
            total=self._podcast_totals.total + 1,
            subscribed=self._podcast_totals.subscribed + 1
            if podcast.is_subscribed
            else self._podcast_totals.subscribed,
        )
        self._episode_totals = EpisodeTotals(
            total=self._episode_totals.total + len(podcast.episodes),
            played=self._episode_totals.played + podcast.total_played,
            not_played=self._episode_totals.not_played + podcast.total_unplayed,
            started=self._episode_totals.started + podcast.total_started,
            visible=self._episode_totals.visible + podcast.total_visible,
        )
        if (
            not self._podcast_least_played_episodes
            or podcast.total_played < self._podcast_least_played_episodes.total_played
        ):
            self._podcast_least_played_episodes = podcast
        if (
            not self._podcast_most_played_episodes
            or podcast.total_played > self._podcast_most_played_episodes.total_played
        ):
            self._podcast_most_played_episodes = podcast

    def stats(self) -> Totals:
        return Totals(podcasts=self._podcast_totals, episodes=self._episode_totals)

    def __str__(self) -> str:
        return f"""Total podcasts: {self._podcast_totals.total} ({self._podcast_totals.subscribed} subscribed)
Total episodes: {self._episode_totals.total} ({self._episode_totals.played} played, {self._episode_totals.not_played} unplayed, {self._episode_totals.started} started) 
Total episodes visible on phone (i.e. eligible to download): {self._episode_totals.visible}
Podcast with most played episodes: {self._podcast_most_played_episodes.name}
Podcast with least played episodes: {self._podcast_least_played_episodes.name}
"""
