#!/usr/bin/env python
'''
	Author			: Chaitanya Kumar Guduru
	Organization	: Teradata
	Tool			: Version Check Tool
	Module_Name		: Main Runner
	Files required	: extractor, file, logger, results, webParser
	Required modules: argparse, getpass, hashlib, HTMLParser, json, os, re, shutil, tarfile, urllib2, urlparse, zipfile
						- few modules may import other python modules internally.
'''

import argparse
import getpass
import os
from src import extractor
from src import file
from src.logger import Logger
from src import results
from src import webParser

def runner():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--verbose", "-v", type=int, help="Increase output verbosity")
        parser.add_argument("--username", "-u", help="Your quicklook user id")
        parser.add_argument("--password", "-p", help="Password for authentication of distribution server")
        parser.add_argument("--primaryRelease", "-r1", help="Primary release number")
        parser.add_argument("--secondaryRelease", "-r2", help="Secondary realease number, if you want to compare Release-to-Release")
        parser.add_argument("--primaryDirectory", "-d1", help="Directory Primary release number")
        parser.add_argument("--secondaryDirectory", "-d2", help="Directory Secondary realease number, if you want to compare Release-to-Release")
        parser.add_argument("--file", "-f", help="if you want to compare Release-to-MasterFile")
        args = parser.parse_args()

        verbose = 1     #Default file verbose, if not passed it is SET to 1
        if args.verbose:
            verbose = args.verbose
        elif args.verbose ==0:
            verbose = 0

        if not os.path.exists('output'):
            os.mkdir('output', 0755)
        if not os.path.exists('tempFiles'):
            os.mkdir('tempFiles', 0755)

        logfile = os.path.join('output', 'Log of Version Check Tool.txt')
        file.exporter('', logfile)
        log = Logger(logfile, verbose)
        log('Starting Master Config Check Tool\n')

        global emptyFiles
        uname = ''
        pswd = ''
        releaseNumber = ''
        releaseName = ''
        releaseDownloadFlag = 0
        if args.username:
            uname = args.username
        else:
            uname = raw_input("User Name\t: ")

        if args.password:
            pswd = args.password
        else:
            if args.primaryRelease or args.secondaryRelease:
                pswd = getpass.getpass("Password\t: ")
        auth = [uname, pswd]

        if args.primaryDirectory:
            releaseNumber = args.primaryDirectory
            releaseName = releaseNumber
        else:
            if args.primaryRelease:
                releaseNumber = args.primaryRelease
                releaseDownloadFlag = 1
            else:
                loopIfWrongInput = True
                while loopIfWrongInput:
                    log('Do you want to input release no (or) Directory containing files?\n Enter "R" for releaseNumber\n Enter "D" for Directory containing files\n')
                input = raw_input('>> ')
                if input == 'R':
                    releaseNumber = raw_input("Enter Release (rXXXXX)\nNumber\t: ")
                    releaseDownloadFlag = 1
                    loopIfWrongInput = False
                elif input == 'D':
                    log('Place all files in TarFiles_<Release_Number_withPrefix\'r\'> under \'tempFiles\' folder and enter only <Release_Number_withPrefix\'r\'> without \'TarFiles_\' prefix\n')
                    releaseName = raw_input('Folder Name: ')
                    releaseNumber = releaseName
                    loopIfWrongInput = False
                else:
                    print 'Invalid choice\n'

        if releaseDownloadFlag == 1:
            releaseName = webParser.parser(releaseNumber, auth, log)
        emptyFiles = extractor.extractAll(releaseNumber, releaseName, log)

        sReleaseName = ''
        releaseNumberFlag = 0
        releaseDirectoryFlag = 0
        if args.file:
            sReleaseName = args.file
        elif args.secondaryRelease:
            secondaryReleaseNumber = args.secondaryRelease
            releaseNumberFlag = 1
        elif args.secondaryDirectory:
            secondaryReleaseNumber = args.secondaryDirectory
            sReleaseName = secondaryReleaseNumber
            releaseDirectoryFlag = 1
        else:
            loopIfWrongInput = True
            while loopIfWrongInput:
                log('Do you want to input other release no (or) Choose Directory of files (or) Upload a .json master config file?\n Enter "R" for releaseNumber\n Enter "F" for master config file\n Enter "D" for Directory containing files\n')
                input = raw_input('>> ')
                if input == 'R':
                    secondaryReleaseNumber = raw_input("Enter Release (rXXXXX)\nNumber\t: ")
                    releaseNumberFlag = 1
                    loopIfWrongInput = False
                elif input == 'F':
                    log('Place JSON file in \'tempFiles\' folder and enter only <FILENAME> without extension\n')
                    sReleaseName = raw_input('File Name: ')
                    loopIfWrongInput = False
                elif input == 'D':
                    log('Place all files in TarFiles_<Release_Number_withPrefix\'r\'> under \'tempFiles\' folder and enter only <Release_Number_withPrefix\'r\'> without \'TarFiles_\' prefix\n')
                    sReleaseName = raw_input('Folder Name: ')
                    secondaryReleaseNumber = sReleaseName
                    releaseDirectoryFlag = 1
                    loopIfWrongInput = False
                else:
                    print 'Invalid choice\n'

        if releaseNumberFlag == 1:
            sReleaseName = webParser.parser(secondaryReleaseNumber, auth, log)
        if (releaseNumberFlag == 1) or (releaseDirectoryFlag == 1):
            emptyFiles += extractor.extractAll(secondaryReleaseNumber, sReleaseName, log)

        releasePName = os.path.join('tempFiles', releaseName)
        PrimaryDict = file.loader(releasePName, log)
        sReleasePName = os.path.join('tempFiles', sReleaseName)
        SecondaryDict = file.loader(sReleasePName, log)

        primaryHashDictPath = os.path.join('tempFiles', releaseName+'_md5')
        PrimaryHashDict = file.loader(primaryHashDictPath, log)
        secondaryHashDictPath = os.path.join('tempFiles', sReleaseName+'_md5')
        SecondaryHashDict = file.loader(secondaryHashDictPath, log)


        data = results.generator(PrimaryDict, SecondaryDict, PrimaryHashDict, SecondaryHashDict, emptyFiles, log)

        outputFileName = 'Comparison of ' + PrimaryDict.keys()[0] + ' & ' + SecondaryDict.keys()[0] + '.csv'
        outputFile = os.path.join('output', outputFileName)
        log('Creating file ' + outputFileName + ' & writing into it.\n', 3)
        file.exporter(data, outputFile)

    except Exception as e:
        log('Got an error, please refer logfile and try again!\n' + str(e))
        raise
    else:
        log('Completed, please check output file: ' + outputFileName + '!\n')

if __name__ == "__main__":
    runner()
