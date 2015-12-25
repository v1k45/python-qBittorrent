===============
Getting started
===============
Python wrapper for qBittorrent Web API (for versions above v3.1.x)
For qBittorents client with earlier versions, use mookfist's `python-qbittorrent <https://github.com/mookfist/python-qbittorrent>`__.

This wrapper is based on the methods described in `qBittorrent's Official Web API Documentation <https://github.com/qbittorrent/qBittorrent/wiki/WebUI-API-Documentation>`__

Some methods are only supported in qBittorent's latest version (v3.3.1 when writing), It'll be best if you upgrade your client to a latest version.

Quick usage guide
=================
.. code-block:: python

    from qbittorrent import Client

    qb = Client('http://127.0.0.1:8080/')

    qb.login('admin', 'your-secret-password')
    # defaults to admin:admin.
    # to use defaults, just do qb.login()

    torrents = qb.torrents()

    for torrent in torrents:
        print torrent['name']

Overview of API methods
=======================

Getting torrents
----------------

- Get all ``active`` torrents::

    qb.torrents()

- Filter torrents::

    qb.torrents(status='downloading', label='my label')
    # This will return all torrents which are currently
    # downloading and are labeled as ``my label``.

    qb.torrents(status='paused', sort='ratio')
    # This will return all paused torrents sorted by their Leech:Seed ratio.

Refer qBittorents WEB API documentation for all possible filters.

Downloading torrents
--------------------

- Download torrents by link::

    magnet_link = "magnet:?xt=urn:btih:e334ab9ddd91c10938a7....."
    qb.download_from_link(link=magnet_link)

    # No matter the link is correct or not,
    # method will always return empty JSON object.

- Download multipe torrents by list of links::

    link_list = [link1, link2, link3]
    qb.download_from_link(link_list=link_list)

- Downloading torrents by file::

    torrent_file = open('my-torrent-file.torrent')
    qb.download_from_file(file_buffer=torrent_file)

- Downloading multiple torrents by using files::

    torrent_file_list = [open('1.torrent'), open('2.torrent')]
    qb.download_from_file(file_buffer_list=torrent_file_list)

- Specifing save path for downloads::

    dl_path = '/home/user/Downloads/special-dir/'
    qb.download_from_file(file_buffer=myfile, save_path=dl_path)

    # same for links.
    qb.download_from_link(link=my_magnet_uri, save_path=dl_path)

- Applying labels to downloads::

    qb.download_from_file(file_buffer=myfile, label='secret-files ;) ')

    # same for links.
    qb.download_from_link(link=my_magnet_uri, label='anime')

Pause / Resume torrents
-----------------------

- Pausing/ Resuming all torrents::

    qb.pause_all()
    qb.resume_all()

- Pausing/ Resuming a speicific torrent::

    info_hash = 'e334ab9ddd91c10938a7a87875aa5d7fff526cb4'
    qb.pause(info_hash)
    qb.resume(info_hash)

- Pausing/ Resuming multiple torrents::

    info_hash_list = ['e334ab9ddd91c10938a7a87875aa5d7fff526cb4',
                      'c9dc36f46d90b0e2f2bfe02ce9ac0f490ebebc46',
                      '4c859243615b106652a6e989d71fdf58b1f20108']

    qb.pause_multiple(info_hash_list)
    qb.resume_multipe(info_hash_list)


Authors
=======

- `Vikas Yadav <https://www.github.com/v1k45/>`__
- Your name here :)