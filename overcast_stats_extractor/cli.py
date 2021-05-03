import argparse
import logging

from overcast_stats_extractor.model import Settings
from overcast_stats_extractor.model.exceptions import (
    NoCache,
    AuthenticationFailed,
    OpmlFetchError,
)
from overcast_stats_extractor.model.settings import CacheOverride
from overcast_stats_extractor.stats import fetch_and_extract

parser = argparse.ArgumentParser()

config_file_group = parser.add_argument_group("Config file")
group = parser.add_argument_group("CLI args")
cache_group = parser.add_mutually_exclusive_group()
cache_group.add_argument(
    "-c",
    "--force-cached",
    action="store_true",
    dest="force_cached",
    help="Force use of the cache file (disallow fetching from Overcast site)",
)
cache_group.add_argument(
    "-f",
    "--force-fresh",
    action="store_true",
    dest="force_fresh",
    help="Force fetching fresh data (beware doing this too frequently!)",
)
group.add_argument("-e", "--email", "-u", "--username", help="Your Overcast email")
group.add_argument("-p", "--password", help="Your Overcast password")
parser.add_argument(
    "-cp",
    "--cache-dir",
    default="/tmp/",
    help="The directory in which to cache the Overcast data. Defaults to '/tmp/'",
)
parser.add_argument(
    "-st",
    "--started-threshold",
    type=int,
    default=60,
    help="The path at which to cache the Overcast data. Defaults to '/tmp/'",
)

logging.basicConfig(
    format="%(asctime)s %(levelname)s - %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def main():
    args = parser.parse_args()
    if not args.force_cached and not (args.email or args.password):
        if args.email and not args.password:
            logger.warning("A password must be supplied")
            parser.print_help()
            exit(1)
        elif args.password and not args.email:
            logger.warning("An email must be supplied")
            parser.print_help()
            exit(1)
        else:
            logger.warning("Username and password must be specified")
            parser.print_help()
            exit(1)
    cache_override = CacheOverride.NORMAL
    if args.force_cached:
        cache_override = CacheOverride.FORCE_CACHED
    if args.force_fresh:
        cache_override = CacheOverride.FORCE_FRESH

    settings = Settings(
        email=args.email,
        password=args.password,
        cache_dir=args.cache_dir,
        started_threshold=args.started_threshold,
        cache_override=cache_override,
    )
    try:
        stats = fetch_and_extract(settings)
        print(stats)
    except NoCache as e:
        logger.debug(e, exc_info=True)
        logger.critical("No cached data found and --force-cached was supplied")
    except AuthenticationFailed or OpmlFetchError:
        logger.critical("Failed to extract stats", exc_info=True)
