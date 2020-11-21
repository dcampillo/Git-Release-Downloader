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
        help='Verbosity of logging: 0 -critical, 1- error, 2 -warning, 3 -info, 4 -debug', choices=[0, 1, 2, 3, 4])
    parser.add_argument("-f", metavar="format", type=str, default='zip', help='Format of the downloaded file : t = Tarball, z = Zip (default)', choices=['zip', 'tar'])
    parser.add_argument("-so", help='Download only the source even if assets are available', action='store_true')
    parser.add_argument("-lo", help='Print source url and skip the download', action='store_true')
    parser.add_argument("-d", help='Debug mode -> skip download the file', action='store_true')
    parser.add_argument("-i", help='Displays information about the repos, Source URLs and assets', action='store_true')

    args = parser.parse_args()
    verbose = {0: logging.CRITICAL, 1: logging.ERROR, 2: logging.WARNING, 3: logging.INFO, 4: logging.DEBUG}
    #logging.basicConfig(filename='app.log', level=verbose[args.v])
    logging.basicConfig(format='%(message)s', level=verbose[args.v], stream=sys.stdout)            
    return args


class RepoDownloadManager:

    RepoName = ''
    RepositoryUrl = ''
    __repoJson = ''
    __assets = []
    __sourceurls = {}
    

    def __init__(self, RepositoryName):
        self.RepoName = RepositoryName
        self.RepositoryUrl = 'https://api.github.com/repos/' + RepositoryName + '/releases/latest'
        self.__repoJson = self.__get_repoinfo(self.RepositoryUrl)
        self.__extract_repoinfo()

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
            critical("General error" + str(e))
            exit()

    def __extract_repoinfo(self):
        self.__sourceurls['zip'] = self.__repoJson['zipball_url']
        self.__sourceurls['tar'] = self.__repoJson['tarball_url']
        if self.__repoJson['assets']:
            __assets = self.__repoJson['assets']

    def __get_fileextension(self, DownloadFormat):
        switcher={
            "tar":".tar.gz", 
            "zip":".zip"
        }
        return switcher.get(DownloadFormat, "Invalid file type format")

    def get_downloadSourceUrl(self, DownloadFormat):
        return self.__sourceurls.get(DownloadFormat)

    
    def DownloadRelease(self, DownloadFormat):

        _fileExtension = self.__get_fileextension(DownloadFormat)

        try:
            print('Downloading latest release!')
            print(self.__sourceurls[DownloadFormat])

            response = requests.get(self.__sourceurls[DownloadFormat], allow_redirects=True)
            
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
        repoMngr = RepoDownloadManager(args.repository)

        if args.i:
            print("Repository name:\t\t%s" % repoMngr.RepoName)
            print("Repository URL:\t\t%s" % repoMngr.RepositoryUrl)
            exit()
            


        if args.d == True:
            print("### DEBUG MODE ###")

        

        print(repoMngr.RepoName)
        print(repoMngr.RepositoryUrl)

        if args.lo == False:
            repoMngr.DownloadRelease(args.f)
        else:
            print(repoMngr.get_downloadSourceUrl(args.f))

    except Exception as e:
        error(str(e))

if __name__ == '__main__':
    args = parse_arguments()
    main()
