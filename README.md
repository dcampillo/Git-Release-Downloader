# Git-Release-Downloader
Simple python script to download Git relase from GitHub

## Usage

usage: gitreleasedownloader.py [-h] [-v verbosity] [-f format] [-d debug] repository

* -v = Verbosity of logging: 0 -critical, 1- error [DEFAULT], 2 -warning, 3 -info, 4 -debug
* -f = Format of the downloaded file: t = Tarball (.tar.gz), t = Zip file (.zip) [DEFAULT] 
* -d = Debug mode: Used only for testing purpose. When enabled the file download is skipped

## Requirements
This scripts relies on the following python libraries:

1. Requests
2. Argparse
