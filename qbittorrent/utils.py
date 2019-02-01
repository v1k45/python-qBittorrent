import re, requests, os, logging

extensions = {
    "image/jpeg": "jpg",
    "image/gif": "gif",
    "video/mp4": "mp4",
    "video/webm": "webm",
}


def download_file(filepath, source_url, options=[]):
    if re.search("^//", source_url):
        source_url = "https:%s" % source_url

    # logging.info("Checking file from %s" % source_url)
    headers = requests.head(source_url).headers

    if headers.get("content-type") not in extensions:
        logging.info("Unable to get extension for %s", headers.get("content-type"))
        quit()

    extension = extensions[headers.get("content-type")]
    filepath = "%s.%s" % (filepath, extension)

    if os.path.isfile(filepath):
        stat = os.stat(filepath)
        if stat.st_size == int(headers.get("content-length")):
            logging.info("File %s exists and is the same size. Skipping." % filepath)
            return

        if stat.st_size > int(headers.get("content-length")):
            logging.info("File %s exists and is bigger. Skipping." % filepath)
            return

        logging.info("File %s exists but is smaller. Downloading." % filepath)

    if "dry-run" in options and options["dry-run"] == True:
        logging.info("Dry run. Not downloading.")
        return

    logging.info("Downloading file %s to %s" % (source_url, filepath))
    dl = requests.get(source_url, stream=True)
    with open("%s.dl" % filepath, "wb") as handle:
        for data in dl.iter_content(chunk_size=512):
            handle.write(data)
        handle.close()
        dl.close()

    os.rename("%s.dl" % filepath, filepath)


def full_path(dir_):
    if dir_[0] == "~" and not os.path.exists(dir_):
        dir_ = os.path.expanduser(dir_)
    return os.path.abspath(dir_)

def sizeof_fmt(num, suffix='B'):
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            if len(str(int(num))) > 1:
                return "%3.0f%s%s" % (num, unit, suffix)
            else:
                return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Y', suffix)

intervals = (
    ('w', 604800),  # 60 * 60 * 24 * 7
    ('d', 86400),    # 60 * 60 * 24
    ('h', 3600),    # 60 * 60
    ('m', 60),
    ('s', 1),
    )

def display_time(seconds, granularity=2):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{}{}".format(value, name))
    return ''.join(result[:granularity])
