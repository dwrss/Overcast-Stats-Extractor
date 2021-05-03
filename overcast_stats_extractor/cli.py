import argparse
import collections

from overcast_stats_extractor.stats import fetch_and_extract

parser = argparse.ArgumentParser()

config_file_group = parser.add_argument_group("Config file")
config_file_group.add_argument("-c", "--config")
group = parser.add_argument_group("CLI args")
group.add_argument("-e", "--email", help="Overcast email")
group.add_argument("-p", "--password", help="Overcase password")

parser.add_argument(
    "-sp",
    "--session-path",
    default="/tmp/.overcast_session",
    help='The path at which to store session data. Defaults to "/tmp/.overcast_session"',
)
parser.add_argument(
    "-cp",
    "--cache-folder",
    default="/tmp/",
    help="The folder in which to cache the Overcast data. Defaults to '/tmp/'",
)
parser.add_argument(
    "-st",
    "--started-threshold",
    type=int,
    default=60,
    help="The path at which to cache the Overcast data. Defaults to '/tmp/'",
)


def main():
    args = parser.parse_args()
    if not args.config and not (args.email and args.password):
        if args.email and not args.password:
            print("A password must be supplied")
            exit(1)
        elif args.password and not args.email:
            print("An email must be supplied")
            exit(1)
        else:
            print("Username and password must be specified via config file or args")
            exit(1)
    stats = fetch_and_extract(args)
    print(stats)
