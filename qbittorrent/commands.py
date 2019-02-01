import logging, os, re, sys, json
from qbittorrent import utils
from functools import partial
from multiprocessing.pool import Pool
from datetime import datetime

# torrent_columns = {
#   "added_on": {
#       "header": "Added",
#       "format": lambda x: time.strftime('%Y-%m-%d', time.localtime(x)),
#   },
#   "amount_left": {
#       "header": "Amt Left",
#       "format": lambda x: utils.sizeof_fmt(x),
#   },
#   "auto_tmm": {
#       "header": "AutoTMM",
#       "format": lambda x: str(x),
#   },
#   "category": {
#       "header": "Cat",
#   },
#   "completed": 120936020,
#   "completion_on": 1548598818,
#   "dl_limit": -1,
#   "dlspeed": 0,
#   "downloaded": 0,
#   "downloaded_session": 0,
#   "eta": 8640000,
#   "f_l_piece_prio": false,
#   "force_start": false,
#   "hash": "e06706041f96f66cf15e20cf79a360081744237a",
#   "last_activity": 0,
#   "magnet_uri": "magnet:?xt=urn:btih:e06706041f96f66cf15e20cf79a360081744237a&dn=Various%20Artists%20-%202009%20-%20Punk%20Goes%20Pop%202%20(320)&tr=https%3a%2f%2fflacsfor.me%2f7f11578756650f76fac09bfdbf1322fa%2fannounce",
#   "max_ratio": -1,
#   "max_seeding_time": -1,
#   "name": "Various Artists - 2009 - Punk Goes Pop 2 (320)",
#   "num_complete": 0,
#   "num_incomplete": 0,
#   "num_leechs": 0,
#   "num_seeds": 0,
#   "priority": 0,
#   "progress": 1,
#   "ratio": 0,
#   "ratio_limit": -2,
#   "save_path": "/torrents/downloads/music/",
#   "seeding_time_limit": -2,
#   "seen_complete": 4294967295,
#   "seq_dl": false,
#   "size": 120936020,
#   "state": "pausedUP",
#   "super_seeding": false,
#   "tags": "",
#   "time_active": 284,
#   "total_size": 120936020,
#   "tracker": "",
#   "up_limit": -1,
#   "uploaded": 0,
#   "uploaded_session": 0,
#   "upspeed": 0
# }


class Downloader(object):
    def __init__(self, save_dir):
        self.save_dir = save_dir

    def __call__(self, image):
        if os.path.isfile(
            "{}/{} - {}".format(self.save_dir, image["id"], image["file"])
        ):
            print("File {} - {} exists. Skipping.".format(image["id"], image["file"]))
            return

        print("Downloading {}".format(image["file"]))
        dl = requests.get(image["element_url"], stream=True)
        with open(
            "{}/{} - {}.dl".format(self.save_dir, image["id"], image["file"]), "wb"
        ) as handle:
            for data in dl.iter_content(chunk_size=512):
                handle.write(data)
            handle.close()
            dl.close()

        os.rename(
            "{}/{} - {}.dl".format(self.save_dir, image["id"], image["file"]),
            "{}/{} - {}".format(self.save_dir, image["id"], image["file"]),
        )


def add_cmd(api, args):
    files = []
    links = []
    for torrent in args.torrents:
        if re.search("^magnet:", torrent):
            links.append(torrent)
        else:
            files.append(open(torrent.encode("utf8", errors="surrogateescape"), "rb").read())

        if len(files) == 10:
            _add(api, args, files=files)
            files = []
        if len(links) == 10:
            _add(api, args, links=links)
            links = []

    if len(files) > 0:
        _add(api, args, files=files)
    if len(links) > 0:
        _add(api, args, links=links)

def _add(api, args, files=[], links=[]):
    data = vars(args)
    data.pop('torrents', None)

    if len(files) > 0:
        logging.info("Adding {} files...".format(len(files)))
        api.download_from_file(files, **data)
    if len(links) > 0:
        logging.info("Adding {} links...".format(len(links)))
        api.download_from_link(links, **data)


def list_cmd(api, args):
    # print("Done\tDown\tUp\tETA\tRatio\tState\t\tName")

    torrents = api.torrents(filter=args.filter, category=args.category)

    if args.search:
        filters = dict(item.split("=") for item in args.search.split(","))
        for key, val in filters.items():
            regex = r"{}".format(val)
            torrents = [t for t in torrents if re.search(regex, t[key], re.IGNORECASE)]

    for torrent in torrents:
        output = "{}%\t{}\t{}\t{}\t{}\t{}\t{}".format(
            int(torrent["progress"] * 100),
            utils.sizeof_fmt(torrent["dlspeed"], "B/s"),
            utils.sizeof_fmt(torrent["upspeed"], "B/s"),
            utils.display_time(torrent["eta"]),
            round(float(torrent["ratio"]), 1),
            torrent["state"],
            torrent["name"],
            torrent["save_path"],
        )

        if args.location:
            api.set_location(torrent['hash'], args.location)
            print("MOVED: {}".format(torrent["name"]))

        if args.pause:
            api.pause(torrent['hash'])
            output = "PAUSED: {}".format(torrent["name"])
        if args.resume:
            api.resume(torrent['hash'])
            output = "RESUMED: {}".format(torrent["name"])
        if args.purge:
            api.delete_permanently(torrent['hash'])
            output = "PURGED: {}".format(torrent["name"])
        elif args.delete:
            api.delete(torrent['hash'])
            output = "DELTED: {}".format(torrent["name"])
        elif args.recheck:
            api.recheck(torrent['hash'])
            output = "RECHECKING: {}".format(torrent["name"])

        print(output)


def prefs_cmd(api, args):
    if len(args.preference) == 1:
        preferences = api.preferences()
        logging.info(
            "{}: {}".format(args.preference[0], preferences[args.preference[0]])
        )
    elif len(args.preference) == 2:
        prefs = {args.preference[0]: args.preference[1]}
        api.set_preferences(**prefs)

        preferences = api.preferences()
        logging.info(
            "Successfully set {}: {}".format(
                args.preference[0], preferences[args.preference[0]]
            )
        )
    else:
        logging.error("Invalid number of arguments")
