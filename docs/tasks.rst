Performing common tasks
=======================

This page is an overview of common actions you'll perform when using this wrapper. Some methods are handled diffently and some are only compatible with the latest versions. It is recommended to update your qBittorrent client to the latest version.

Since we dicussed about download and pause methods on the previous page, we'll be skipping them here.

Please refer `Full API method list <modules/api.html>`__

Getting version details
-----------------------

- Get version info of qBittorrent client::

    In [4]: qb.qbittorrent_version
    Out[4]: u'v3.3.1'

- Get API Min and Max version::

    In [6]: qb.api_version
    Out[6]: 7

    In [7]: qb.api_min_version
    Out[7]: 2

Handling added torrents
-----------------------

- Add trackers to a torrent::

    In [11]: tracker = 'udp://my.prvt.site:1337/announce'

    In [12]: infohash = '0e6a7....infohash....5db6'

    In [13]: qb.add_trackers(infohash, tracker)
    Out[13]: {} # No matter if method fails, it always returns {}.

    # to add multiple trackers, add a like break ('%0A') b/w trackers.

- Deleting torrents::

    infohash_list = 'A single infohash or a list() of info hashes'

    qb.delete(infohash_list) # for deleting entry from qBittorrent.

    qb.delete_permanently(infohash_list) # delete it from disk too.

- Global speed limit values::

    In [14]: qb.global_download_limit
    Out[14]: 0

    In [15]: qb.global_upload_limit
    Out[15]: 51200

    In [16]: qb.global_upload_limit = 102400

    In [17]: qb.global_upload_limit
    Out[17]: 102400

- Preferences::

    qb.preferences() # for getting dictionary of setting vaulues

    qb.preferences['setting_name'] # for fetching a particular setting

    qb.preferences['setting_name'] = 'setting-value' # for changing a setting value.

    # example

    In [20]: prefs = qb.preferences()

    In [21]: prefs['autorun_enabled']
    Out[21]: True

    In [22]: prefs['autorun_enabled'] = False

    In [23]: prefs['autorun_enabled']
    Out[23]: False

    # changing multiple settings at once:

    qb.set_preferences(setting_name1=setting_value1, setting_name2=setting_value2,
                       setting_nameN=setting_valueN)

- Misc::

    qb.shutdown() # shutdown qbittorrent

    qb.toggle_sequential_download() # as it says

    qb.logout() # logs out of current session.

This page was just for important methods, Please refer `Full API method list <modules/api.html>`__
