#!/usr/bin/env cdat
# -*-coding:Latin-1 -*
# Created : 2014/01 (A. Germe)
# Modified: no 00
# Principal component Analysis
#======================================================================== 
import sys, os
import netCDF4 as nc
import datetime
import copy
import MA
import numpy as N
#
from direxp import *
import climtools as ct
#======================================================================== 

MM=M
Mcenter = MM - MM.mean(axis=0)
MCOV = N.cov(Mcenter.transpose())
EVAL,EVEC = N.linalg.eig(MCOV)
PROJ = N.dot(Mcenter,EVEC)
varexp = 100 * EVAL/sum(EVAL) 
