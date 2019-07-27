#!/usr/bin/env python
'''
	Author			: Chaitanya Kumar Guduru
	Organization	: Teradata
	Tool			: Version Check Tool
	Module_Name		: extractor
'''

import hashlib
import json
import os
import re
import shutil
import tarfile
import zipfile

def md5(fname, log):
   hash_md5 = hashlib.md5()
   log('\t\tCalculating #MD5 for '+fname+'\n', 3)
   with open(fname, "rb") as f:
      for chunk in iter(lambda: f.read(4096), b""):
         hash_md5.update(chunk)
   return hash_md5.hexdigest()

def untar(fname, path, parentFile, log):
   log('\n\t--Processing: '+fname+'\n', 3)
   tar_args = 'r'
   tar_module = ''
   parentFile.extract(fname, path)			#Extract file inside parentCompressed file
   tmpFileLoc = os.path.join(path, fname)	#Set location of the file, for further access
   md5sum =  md5(tmpFileLoc, log)
   log('\t\t---'+ tmpFileLoc+' : '+md5sum, 3)

   if re.search( r'(.*).(gz|tar)$', fname, re.I | re.M):
      tar_module = 'tarfile'
   elif re.search( r'.*\.(zip)$', fname, re.I | re.M):
      tar_module = 'zipfile'
   else:
      shutil.rmtree(path)
      return md5sum

   fileCount=0
   if tar_module == 'tarfile':
      extractFileObject = tarfile.open(tmpFileLoc, tar_args)
      fileCount = len(extractFileObject.getmembers())
   else:
      extractFileObject = zipfile.ZipFile(tmpFileLoc, tar_args)
      fileCount = len(extractFileObject.infolist())  
   extractFileObject.close()

   global emptyFiles
   if fileCount == 0:
      emptyFiles.append(tmpFileLoc)

   shutil.rmtree(path)
   return md5sum

def extractor(fname, releaseName, log):
   log('\n-Processing '+fname+'...', 3)
   tar_args = 'r'
   tar_module = ''

   if re.search( r'(.*).(gz|tar)$', fname, re.I | re.M):
      tar_module = 'tarfile'
   elif re.search( r'.*\.(zip)$', fname, re.I | re.M):
      tar_module = 'zipfile'
   else:
      return fname

   listDict = {}
   hashDict = {}
   FileLoc = os.path.join(TarFolder, fname)

   #File Info()- List of files, inside Zip/Tar file
   if tar_module == 'tarfile':
      file = tarfile.open(FileLoc, tar_args)
      fileInfo = file.getmembers()
   else:
      file = zipfile.ZipFile(FileLoc, tar_args)
      fileInfo = file.infolist()
	  
   #Empty file:
   global emptyFiles
   if len(fileInfo) == 0:
      emptyFiles.append(FileLoc)
   elif len(fileInfo) == 1:
      if tar_module == 'tarfile' and fileInfo[0].type == '5':
            emptyFiles.append(FileLoc)
      elif re.search(r'(.*).(/)$', fileInfo[0].filename, re.M):
            emptyFiles.append(FileLoc)
   else:
   #Checking for files inside Tar/Zip
      for mem in fileInfo:
         path = os.path.join(TarFolder, releaseName)
         if tar_module == 'tarfile' and mem.type == '0':
            hash = untar(mem.name, path, file, log)
            listDict.update({mem.name:mem.size})
            hashDict.update({mem.name:hash})
         elif tar_module == 'zipfile' and not re.search(r'(.*).(/)$', mem.filename, re.M):
            hash = untar(mem.filename, path, file, log)
            listDict.update({mem.filename:mem.file_size})
            hashDict.update({mem.filename:hash})
   return [listDict, hashDict]

def extractAll(releaseNumber, releaseName, log):
   global TarFolder, emptyFiles

   
   log('\nExtraction of '+ releaseNumber+ ', started', 2)
   
   emptyFiles = []
   TarFolder = os.path.join('tempFiles', 'TarFiles_'+releaseNumber)
   fileDict  = {}
   md5Dict   = {}
   
   for files in os.listdir(TarFolder):
      key = files
      if re.search(r'Analytics_(.*).(zip)$', files):
         key = re.search(r'Analytics_([^__]+)', files).group(1)
      elif re.search(r'Analytics', files):
         log('Individual files: '+key, 3)
      elif re.search(r'__([^\.]+)', files):
         key = re.search(r'__([^\.]+)', files).group(1)
      dictArray = extractor(files, releaseName, log)
      fileDict[key] = dictArray[0]
      md5Dict[key]  = dictArray[1]

   #shutil.rmtree(TarFolder)
   fileName = releaseName+'.json'
   filepath = os.path.join('tempFiles', fileName)
   if os.path.isfile(filepath):
      os.remove(filepath)
   log('Creating file: '+fileName, 2)
   with open(filepath, 'w+') as f:
      json.dump({releaseName: fileDict}, f, sort_keys=True, indent =4, separators=(',', ': '))


   fileName = releaseName+'_md5.json'
   filepath = os.path.join('tempFiles', fileName)
   if os.path.isfile(filepath):
      os.remove(filepath)
   log('\nCreating file: '+fileName, 2)
   with open(filepath, 'w+') as f:
      json.dump({releaseName: md5Dict}, f, sort_keys=True, indent =4, separators=(',', ': '))

   log('\nExtraction of '+ releaseNumber+ ', successful to '+ fileName+'\n')
   
   return emptyFiles
