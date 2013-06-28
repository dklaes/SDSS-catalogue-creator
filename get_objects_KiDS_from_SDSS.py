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
# $6	camera

#Importing packages
import os
import sys
import numpy as np
import astropy
import astropy.io as io
import astropy.io.fits as fits


# Reading command line arguments
PATH = sys.argv[1]
#TYPES = sys.argv[2]
TYPES = ['SCIENCE']
SAVETOPATH = sys.argv[3]
CATALOG = sys.argv[4]
#FILTER = sys.argv[5]
#FILTERS = ['r_SDSS', 'g_SDSS', 'u_SDSS', 'i_SDSS', 'z_SDSS']
FILTERS = ['r_SDSS']
#CAMERA = sys.argv[6]
CAMERA = 'OMEGACAM@VST'

# Some configuration
GETSDSS="/vol/science01/scratch/dklaes/data/SDSSR9_query/SDSSR7_objects.py"

CAMERAS = np.loadtxt("cameras.ini", delimiter="\t", dtype={'names': ('THELI_name', 'RA_name', 'DEC_name', 'FOV_x_deg', 'FOV_y_deg'), 'formats': ('S50', 'S10', 'S10', 'S50', 'S50')})

RA=''
DEC=''
for i in range(len(CAMERAS)):
  if CAMERAS[i][0] == CAMERA:
    RA = CAMERAS[i][1]
    DEC = CAMERAS[i][2]
    FOVX = float(CAMERAS[i][3])
    FOVY = float(CAMERAS[i][4])

if RA == '':
  print("No RA key word for " + CAMERA + " not found!")
elif DEC == '':
  print("No DEC key word for " + CAMERA + " not found!")


PWD=os.getcwd()
array = []

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
	array.append(os.getcwd() + "/" + FILES[l])
      
      os.chdir(PATH + "/" + FILTERS[i])
      
      
# later for RA, DEC extraction
array2 = np.array([])
for i in range(len(array)):
  file = fits.open(array[i])
  RAVAL = float(file[0].header[RA])
  DECVAL = float(file[0].header[DEC])
  file.close()
  array2 = np.append(array2,[RAVAL,DECVAL])
array2 = array2.reshape((-1,2))

print(array2[:,0])

# Calculating 
RAMIN = np.array(array2[:,0]-FOVX/2.0)
RAMAX = np.array(array2[:,0]+FOVX/2.0)
DECMIN = np.array(array2[:,1]-FOVY/2.0)
DECMAX = np.array(array2[:,1]+FOVY/2.0)

print(RAMIN)

DECMIN = np.where(DECMIN<-90.0, (-180.0-DECMIN, RAMIN+180.0, RAMAX+180.0), DECMIN)
DECMAX = np.where(DECMAX>90.0, (180.0-DECMAX, RAMIN+180.0, RAMAX+180.0), DECMAX)

RAMIN = np.where(RAMIN<0, RAMIN+360.0, RAMIN)
RAMAX = np.where(RAMIN>360.0, RAMIN-360.0, RAMAX)



print(RAMIN)