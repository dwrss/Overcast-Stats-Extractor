from xml.etree import ElementTree
from datetime import datetime
from dateutil.tz import UTC
from dateutil.parser import parse as parse_dt


from overcast_stats_extractor.model import Podcast, Episode, PodcastStats
from overcast_stats_extractor.overcast_data import Cache, fetch_fresh_data


def extract_stats(opml_content: str, started_threshold: int) -> PodcastStats:
    # parse the OPML
    tree = ElementTree.fromstring(opml_content)

    # find all podcasts and their episodes
    podcasts = tree.findall(".//*[@type='rss']")

    # look for recently played episodes
    now = datetime.utcnow().astimezone(UTC)
    podcast_stats = PodcastStats()

    for podcast in podcasts:
        curr_pod = Podcast(
            name=podcast.attrib["title"],
            is_subscribed=podcast.attrib.get("subscribed", "0") == "1",
        )
        for episode in list(podcast):
            played = episode.attrib.get("played", "0") == "1"
            user_activity_date_raw = episode.attrib.get("userUpdatedDate")
            user_activity_date = parse_dt(user_activity_date_raw)
            episode_details = Episode(
                title=episode.attrib["title"],
                is_deleted=episode.attrib.get("userDeleted", "0") == "1",
                is_started=int(episode.attrib.get("progress", "0")) > started_threshold,
                was_played=played,
                last_modified=user_activity_date,
            )
            curr_pod.add(episode_details)
        podcast_stats.add(curr_pod)
    return podcast_stats


def fetch_and_extract(settings) -> PodcastStats:
    fetcher = Cache(cache_path=settings.cache_dir)
    data = fetcher.read_cached_data()
    if not data:
        # cache the last OPML file
        response = fetch_fresh_data(settings)
        fetcher.write_cached_data(response.text)
        data = response.text
    return extract_stats(data, settings.started_threshold)