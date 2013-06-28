#!/usr/bin/python
# -*- coding: utf-8 -*-
#scipy-0.11 and numpy-1.6.2 required!

# ----------------------------------------------------------------
# File Name:           get_objects_KiDS_from_SDSS.py
# Author:              Dominik Klaes (dklaes@astro.uni-bonn.de)
# Last modified on:    28.06.2013
# Version:		V1.0
# Description:         Get objects for KiDS data from SDSS database
# ----------------------------------------------------------------

# $1	main directory of runs
# $2	type of files (STANDARD, SCIENCE or SCIENCESHORT)
# $3	directory where to save catalogue
# $4	name of the final catalog
# $5	filter

#Importing packages
import os
import sys
import astropy
import astropy.io as io
import astropy.io.fits as fits


# Reading command line arguments
PATH = sys.argv[1]
#TYPES = sys.argv[2]
TYPES = ['STANDARD', 'SCIENCE']
SAVETOPATH = sys.argv[3]
CATALOG = sys.argv[4]
#FILTER = sys.argv[5]
#FILTERS = ['r_SDSS', 'g_SDSS', 'u_SDSS', 'i_SDSS', 'z_SDSS']
FILTERS = ['r_SDSS']

# Some configuration
GETSDSS="/vol/science01/scratch/dklaes/data/SDSSR9_query/SDSSR7_objects.py"

PWD=os.getcwd()

for i in range(len(FILTERS)):
  os.chdir(PATH + "/" + FILTERS[i])
  LIST = os.listdir(os.getcwd())
  
  for j in range(len(LIST)):
    print("\nGetting coordinates from filter " + FILTERS[i] + " in directory " + LIST[j] + "...")
    
    for k in range(len(TYPES)):
      os.chdir(os.getcwd() + "/" + LIST[j] + "/" + TYPES[k] + "_" + FILTERS[i] + "/ORIGINALS/")
      FILES = os.listdir(os.getcwd())
      print(os.listdir(os.getcwd()))
      print("\n")
      
      for l in range(len(FILES)):
	file = fits.open(FILES[l])
	print(file[0].header['AIRMASS'])
	file.close()
      
      os.chdir(PATH + "/" + FILTERS[i])