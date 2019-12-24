import os
from setuptools import setup, find_packages

install_requires = open('requirements.txt').read().splitlines()

__version__ = '0.4.1'


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''


setup(
    name='python-qbittorrent',
    description='Python wrapper for qBittorrent >4.1.x',
    version=__version__,
    long_description=read('README.rst'),
    license='The MIT License',
    platforms=['OS Independent'],
    keywords='torrent, qBittorent, API, wrapper',
    author='Vikas Yadav',
    author_email='v1k45x@gmail.com',
    url="https://github.com/v1k45/python-qbittorrent",
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console'
    ]
)
