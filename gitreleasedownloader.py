#!/usr/bin/env python3
# Project: Git Release Downloader
# File name: gitreleasedownloader.py
# Description: Simple GitHub release downloader
# Author: David Campillo
# Date: 19-11-2020

import sys
import argparse
import requests
import json
import logging
from logging import critical, error, info, warning, debug

#logging.basicConfig(format='%(message)s', level=logging.DEBUG, stream=sys.stderr)
#logging.basicConfig(filename='app.log',level=logging.DEBUG)

def parse_arguments():
    """Read arguments from a command line."""
    parser = argparse.ArgumentParser(description='Arguments get parsed via --commands')
    parser.add_argument('repository', help='Name of the target Git Repositoy')
    parser.add_argument('-v', metavar='verbosity', type=int, default=3,
        help='Verbosity of logging: 0 -critical, 1- error, 2 -warning, 3 -info, 4 -debug')
    parser.add_argument("-f", metavar="format", type=str, default='z', help='Format of the downloaded file : t = Tarball, z = Zip (default)')
    parser.add_argument("-d", metavar="debug", type=bool, default=False, help='Debug mode -> skip download the file')

    args = parser.parse_args()
    verbose = {0: logging.CRITICAL, 1: logging.ERROR, 2: logging.WARNING, 3: logging.INFO, 4: logging.DEBUG}
    #logging.basicConfig(filename='app.log', level=verbose[args.v])
    logging.basicConfig(format='%(message)s', level=verbose[args.v], stream=sys.stdout)            
    return args


class RepoDownloadManager:

    RepoName = ''
    RepositoryUrl = ''
    __repoJson = ''

    def __init__(self, RepositoryName):
        self.RepoName = RepositoryName
        self.RepositoryUrl = 'https://api.github.com/repos/' + RepositoryName + '/releases/latest'
        self.__repoJson = self.__get_repoinfo(self.RepositoryUrl)

    def __get_repoinfo(self, repo_url):
        try:
            response = requests.get(repo_url)
            if response.status_code == 200:
                return json.loads(response.text)
            elif response.status_code == 404:
                error("No release found for repository " + self.RepoName)
                exit()
            else:
                error("Unable to retrieve informaiton for repository " + self.RepoName)
                exit()
        except Exception as e:
            error("General error" + str(e))


    def __get_fileextension(self, DownloadFormat):
        switcher={
            "t":".tar.gz", 
            "z":".zip"
        }
        return switcher.get(DownloadFormat, "Invalid file type format")

    def __get_downloadUrl(self, DownloadFormat):
        
        downloadUrl = ''

        if args.f == 'z':
            downloadUrl = self.__repoJson['zipball_url']
        else:
            downloadUrl = self.__repoJson['tarball_url']
        return downloadUrl

    def DownloadRelease(self, DownloadFormat):

        _fileExtension = self.__get_fileextension(DownloadFormat)

        try:
            print('Downloading latest release!')
            print(self.__get_downloadUrl(DownloadFormat))

            response = requests.get(self.__get_downloadUrl(DownloadFormat), allow_redirects=True)
            
            if response.status_code != 200:
                error("Unable to download file " + self.RepositoryUrl)
                error(self.RepositoryUrl + " | status code: " + str(response.status_code))     
                print('Exiting') 
                exit()
            
            print('Saving file')
            _file = open("output" + _fileExtension, 'wb')
            _file.write(response.content)
            _file.close()
            print('Downloaded!')

        except Exception as e:
            error("Unable to download file " + self.RepositoryUrl)
            error(str(e))

def main():
    try:
        if args.d == True:
            print("### DEBUG MODE ###")
        repoMngr = RepoDownloadManager(args.repository)
        if args.d == False:
            repoMngr.DownloadRelease(args.f)

    except Exception as e:
        error(str(e))

if __name__ == '__main__':
    args = parse_arguments()
    main()
