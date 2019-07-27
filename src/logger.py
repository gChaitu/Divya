#!/usr/bin/env python
'''
	Author			: Chaitanya Kumar Guduru
	Organization	: Teradata
	Tool			: Version Check Tool
	Module_Name		: Output file logger
'''

class Logger:
   def __init__(self, file, verbose):
      self.verbose = verbose
      self.file = file

   def __call__(self, data, verbose=1): #Default line verbose, if not passed it is SET to 0
      f = open(self.file, 'a+')
      f.write(data)
      f.close()

      if verbose <= self.verbose:
         print data.replace('\n', '')
