#!/usr/bin/env python
import qbittorrent, os, sys, argparse, configparser, logging
from qbittorrent import commands, utils

config = {
    "list": {"desc": "List torrents"},
    "add": {"desc": "Add torrent files or links"},
    "prefs": {"desc": "Get and set qBittorrent preferences"}
}


class cli:
    config = None
    api = None

    def __init__(self):
        usage = """qb <command> [<args>]

Commands
"""

        for command in config:
            usage = "{}  {}\t{}\n".format(usage, command, config[command]["desc"])

        parser = argparse.ArgumentParser(usage=usage)
        parser.add_argument("command", help="Command to execute")
        args = parser.parse_args(sys.argv[1:2])

        if not hasattr(self, args.command):
            print("Invalid command %s" % args.command)
            parser.print_help()
            exit(1)

        getattr(self, args.command)()

    def read_config(self, args):
        self.config = configparser.ConfigParser()
        try:
            open(args.config)
            self.config.read(args.config)
        except:
            if not os.path.exists(os.path.dirname(args.config)):
                os.makedirs(os.path.dirname(args.config))
            self.config.add_section("qbittorrent")
            self.config.set("qbittorrent", "host", "")
            self.config.set("qbittorrent", "username", "")
            self.config.set("qbittorrent", "password", "")
            self.config.write(open(args.config, "w"))
            print("Please edit the configuration file: %s" % args.config)
            sys.exit(2)

    def add_global_opts(self, parser):
        parser.add_argument(
            "--config",
            help="The location of the configuration file",
            default=os.path.expanduser("~/.qbittorrent-cli/config"),
        )
        parser.add_argument("--log", help="increase output verbosity", default="INFO")
        return parser

    def list(self):
        parser = argparse.ArgumentParser(
            usage="qb list [<args>]", description="List torrents"
        )
        parser.add_argument("-f", "--filter", help="Filter for status")
        parser.add_argument("-c", "--category", help="Filter for category")
        parser.add_argument("-s", "--search", help="Search torrents")
        parser.add_argument("-l", "--location", help="Set torrent location")
        parser.add_argument("-p", "--pause", help="Pause filtered torrents", action="store_true")
        parser.add_argument("-r", "--resume", help="Resume filtered torrents", action="store_true")
        parser.add_argument("--recheck", help="Recheck filtered torrents", action="store_true")
        parser.add_argument("--delete", help="Delete filtered torrents", action="store_true")
        parser.add_argument("--purge", help="Delete filtered torrents (removing files)", action="store_true")
        # parser.add_argument(
        #     "--columns",
        #     help="Show listed columns",
        #     default="progress,dlspeed,upspeed,eta,ratio,state,name",
        # )
        parser = self.add_global_opts(parser)
        args = parser.parse_args(sys.argv[2:])

        self.setup(args)

        commands.list_cmd(self.client, args)

    def prefs(self):
        parser = argparse.ArgumentParser(
            usage="qb prefs [<args>]", description="Get and set qBittorrent preferences"
        )
        parser.add_argument("preference", nargs="*", help="preference to get or set")
        parser = self.add_global_opts(parser)
        args = parser.parse_args(sys.argv[2:])

        self.setup(args)

        commands.prefs_cmd(self.client, args)

    def add(self):
        parser = argparse.ArgumentParser(
            usage="qb list [<args>]", description="Add torrents"
        )
        parser.add_argument("torrents", nargs="*", help="Torrent files or links")
        parser.add_argument("-s", "--savepath", help="Download save path")
        parser.add_argument("-c", "--category", help="Add to category")
        parser.add_argument("--skip-checking", help="Skip hash check", action="store_true")
        parser = self.add_global_opts(parser)
        args = parser.parse_args(sys.argv[2:])

        self.setup(args)

        commands.add_cmd(self.client, args)

    def setup(self, args):
        numeric_level = getattr(logging, args.log.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError("Invalid log level: %s" % args.log.upper())

        logging.basicConfig(level=numeric_level, format="%(levelname)s:\t%(message)s")

        self.read_config(args)

        self.client = qbittorrent.Client(self.config.get("qbittorrent", "host"))
        self.client.login(
            self.config.get("qbittorrent", "username"),
            self.config.get("qbittorrent", "password"),
        )


def main():
    cli()


if __name__ == "__main__":
    main()
