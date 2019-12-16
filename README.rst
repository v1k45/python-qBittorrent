==================
python-qBittorrent
==================

.. image:: https://readthedocs.org/projects/python-qbittorrent/badge/?version=latest
   :target: http://python-qbittorrent.readthedocs.org/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://badge.fury.io/py/python-qbittorrent.svg
   :target: https://badge.fury.io/py/python-qbittorrent

Python wrapper for qBittorrent Web API (for versions above 4.1, for version below and above v3.1.x please use 0.3.1 version).

For qBittorrent clients with earlier versions, use *mookfist's* `python-qbittorrent <https://github.com/mookfist/python-qbittorrent>`__.

This wrapper is based on the methods described in `qBittorrent's Official Web API Documentation <https://github.com/qbittorrent/qBittorrent/wiki/Web-API-Documentation>`__

Some methods are only supported in qBittorent's latest version (v3.3.1 when writing).

It'll be best if you upgrade your client to a latest version.

Installation
============

The best way is to install a stable release from PyPI::

    $ pip install python-qbittorrent

You can also stay on the bleeding edge of the package::

    $ git clone https://github.com/v1k45/python-qBittorrent.git
    $ cd python-qBittorrent
    $ python setup.py install

Prerequisite
============

qBittorent webUI must be enabled before using this API client. `How to enable the qBittorrent Web UI <https://github.com/lgallard/qBittorrent-Controller/wiki/How-to-enable-the-qBittorrent-Web-UI>`_

Quick usage guide
=================
.. code-block:: python

    from qbittorrent import Client

    qb = Client('http://127.0.0.1:8080/')

    qb.login('admin', 'your-secret-password')
    # not required when 'Bypass from localhost' setting is active.
    # defaults to admin:admin.
    # to use defaults, just do qb.login()

    torrents = qb.torrents()

    for torrent in torrents:
        print torrent['name']

API methods
===========

Getting torrents
----------------

- Get all ``active`` torrents::

    qb.torrents()

- Filter torrents::

    qb.torrents(filter='downloading', category='my category')
    # This will return all torrents which are currently
    # downloading and are labeled as ``my category``.

    qb.torrents(filter='paused', sort='ratio')
    # This will return all paused torrents sorted by their Leech:Seed ratio.

Refer qBittorents WEB API documentation for all possible filters.

Downloading torrents
--------------------

- Download torrents by link::

    magnet_link = "magnet:?xt=urn:btih:e334ab9ddd91c10938a7....."
    qb.download_from_link(magnet_link)

    # No matter the link is correct or not,
    # method will always return empty JSON object.

- Download multipe torrents by list of links::

    link_list = [link1, link2, link3]
    qb.download_from_link(link_list)

- Downloading torrents by file::

    torrent_file = open('my-torrent-file.torrent', 'rb')
    qb.download_from_file(torrent_file)

- Downloading multiple torrents by using files::

    torrent_file_list = [open('1.torrent', 'rb'), open('2.torrent', 'rb')]
    qb.download_from_file(torrent_file_list)

- Specifing save path for downloads::

    dl_path = '/home/user/Downloads/special-dir/'
    qb.download_from_file(myfile, savepath=dl_path)

    # same for links.
    qb.download_from_link(my_magnet_uri, savepath=dl_path)

- Applying labels to downloads::

    qb.download_from_file(myfile, label='secret-files ;) ')

    # same for links.
    qb.download_from_link(my_magnet_uri, category='anime')

Pause / Resume torrents
-----------------------

- Pausing/ Resuming all torrents::

    qb.pause_all()
    qb.resume_all()

- Pausing/ Resuming a speicific torrent::

    info_hash = 'e334ab9ddd....infohash....5d7fff526cb4'
    qb.pause(info_hash)
    qb.resume(info_hash)

- Pausing/ Resuming multiple torrents::

    info_hash_list = ['e334ab9ddd9......infohash......fff526cb4',
                      'c9dc36f46d9......infohash......90ebebc46',
                      '4c859243615......infohash......8b1f20108']

    qb.pause_multiple(info_hash_list)
    qb.resume_multipe(info_hash_list)


Full API method documentation
=============================

All API methods of qBittorrent are mentioned @ `Read the docs <http://python-qbittorrent.readthedocs.org/en/latest/?badge=latest>`__

Authors
=======

Maintainer
----------

- `Vikas Yadav (v1k45) <https://www.github.com/v1k45/>`__

Contributors
------------

*By chronological order*

- `Matt Smith (psykzz) <https://github.com/psykzz>`__
- `Nicolas Wright (dozedoff) <https://github.com/dozedoff>`__
- `sbivol <https://github.com/sbivol>`__
- `Christophe Ha (Shaance) <https://github.com/Shaance>`__
- Your name here :)

TODO
====

- Write tests
