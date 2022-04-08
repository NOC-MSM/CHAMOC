#!/usr/bin/env cdat
# -*-coding:Latin-1 -*
#===========================================================================
import sys, os
import netCDF4 as nc
import datetime
import numpy.ma as ma
import numpy as np
#
import matplotlib as mpl
mpl.rcParams['lines.linewidth'] = 2
mpl.rcParams['axes.linewidth'] = 2
mpl.rcParams['axes.titlesize'] = 18
mpl.rcParams['axes.titleweight'] = 'bold'
mpl.rcParams['axes.labelsize'] = 14
mpl.rcParams['xtick.major.width'] = 2
mpl.rcParams['ytick.major.width'] = 2
mpl.rcParams['xtick.direction'] = 'out'
mpl.rcParams['ytick.direction'] = 'out'
mpl.rcParams['xtick.labelsize'] = 12
mpl.rcParams['ytick.labelsize'] = 12
mpl.rcParams['ps.useafm'] = True
mpl.rcParams['pdf.use14corefonts'] = True
# Issues with tex on JASMIN, so set this to False...
mpl.rcParams['text.usetex'] = False
mpl.rcParams['font.family']= 'sans-serif'
mpl.rcParams['font.sans-serif'] = 'Helvetica'
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D    
from mpl_toolkits.axes_grid1 import make_axes_locatable
#
import climtools as ct
#===========================================================================
#
fileclimmean  = '../data/data_figure_01a.nc'
#
filespread       = '../data/data_figure_06a_var.nc'
filespreadBTR    = '../data/data_figure_06c_BTR_ensvar.nc'
filespreadRES    = '../data/data_figure_06c_RES_ensvar.nc'
filespreadGEO    = '../data/data_figure_06c_GEO_ensvar.nc'
filespreadGEOBTR = '../data/data_figure_06c_GEOBTR_ensvar.nc'

fileclimvar       = '../data/data_figure_02a.nc'
fileclimvarBTR    = '../data/ORCA0083-N06_timestd_19602012_BTRvalor_d05.nc'
fileclimvarRES    = '../data/ORCA0083-N06_timestd_19602012_RESvalor_d05.nc'
fileclimvarGEO    = '../data/ORCA0083-N06_timestd_19602012_GEOvalor_d05.nc'
fileclimvarGEOBTR = '../data/ORCA0083-N06_timestd_19602012_GEOBTRvalor_d05.nc'
#===========================================================================
if not os.path.exists(filespread) :
    sys.exit('The data file does not exit, I quit !')
#
# readfile
# -------
ncid = nc.Dataset(filespread)
tabspread = np.squeeze(ncid.variables['zomsfatl_ES_av'][:,:,:,:])
depth    = ncid.variables["depthw"][:]
lat      = np.squeeze(ncid.variables["nav_lat"][:,:])
ncid.close()
#
ncid = nc.Dataset(fileclimvar)
tabclimvar  = np.squeeze(ncid.variables['zomsfatl'][:,:,:,:])
ncid.close()
#
ncid = nc.Dataset(fileclimmean)
tabclimmean  = np.squeeze(ncid.variables['zomsfatl'][:,:,:,:])
ncid.close()
#
#
ncid = nc.Dataset(filespreadBTR)
tabspreadBTR  = np.squeeze(ncid.variables['BTR_ES'][:,:,:,:])
depthBTR      = ncid.variables["deptht"][:]
latBTR        = np.squeeze(ncid.variables["nav_lat"][:,:])
ncid.close()
#
ncid = nc.Dataset(filespreadRES)
tabspreadRES  = np.squeeze(ncid.variables['RES_ES'][:,:,:,:])
ncid.close()
#
ncid = nc.Dataset(filespreadGEO)
tabspreadGEO  = np.squeeze(ncid.variables['GEO_ES'][:,:,:,:])
ncid.close()
#
ncid = nc.Dataset(filespreadGEOBTR)
tabspreadGEOBTR  = np.squeeze(ncid.variables['GEOBTR_ES'][:,:,:,:])
ncid.close()
#
ncid = nc.Dataset(fileclimvarBTR)
tabclimvarBTR  = np.squeeze(ncid.variables['BTR'][:,:,:,:])
ncid.close()
#
ncid = nc.Dataset(fileclimvarGEO)
tabclimvarGEO  = np.squeeze(ncid.variables['GEO'][:,:,:,:])
ncid.close()
#
ncid = nc.Dataset(fileclimvarRES)
tabclimvarRES  = np.squeeze(ncid.variables['RES'][:,:,:,:])
ncid.close()
#
ncid = nc.Dataset(fileclimvarGEOBTR)
tabclimvarGEOBTR  = np.squeeze(ncid.variables['GEOBTR'][:,:,:,:])
ncid.close()
#
print(tabspread.shape)
print(tabclimvar.shape)
print(tabclimmean.shape)
#
# Convert data into masked array
# ------------------------------
tabspread       = np.nan_to_num( tabspread  )
tabspreadBTR    = np.nan_to_num( tabspreadBTR   )
tabspreadRES    = np.nan_to_num( tabspreadRES   )
tabspreadGEO    = np.nan_to_num( tabspreadGEO   )
tabspreadGEOBTR = np.nan_to_num( tabspreadGEOBTR)
tabclimvar       = np.nan_to_num( tabclimvar      )
tabclimvarBTR    = np.nan_to_num( tabclimvarBTR   )
tabclimvarRES    = np.nan_to_num( tabclimvarRES   )
tabclimvarGEO    = np.nan_to_num( tabclimvarGEO   )
tabclimvarGEOBTR = np.nan_to_num( tabclimvarGEOBTR)
tabspread       = ma.masked_values( tabspread,      0.)
tabspreadBTR    = ma.masked_values( tabspreadBTR,   0.)
tabspreadRES    = ma.masked_values( tabspreadRES,   0.)
tabspreadGEO    = ma.masked_values( tabspreadGEO,   0.)
tabspreadGEOBTR = ma.masked_values( tabspreadGEOBTR,0.)
tabclimvar       = ma.masked_values( tabclimvar,      0.)
tabclimvarBTR    = ma.masked_values( tabclimvarBTR,   0.)
tabclimvarRES    = ma.masked_values( tabclimvarRES,   0.)
tabclimvarGEO    = ma.masked_values( tabclimvarGEO,   0.)
tabclimvarGEOBTR = ma.masked_values( tabclimvarGEOBTR,0.)
#
tabclimmean = np.nan_to_num( tabclimmean)
tabclimmean = ma.masked_values( tabclimmean,0.)
#
tabclimvar       = ma.power(tabclimvar,      2)
tabclimvarBTR    = ma.power(tabclimvarBTR,   2)
tabclimvarRES    = ma.power(tabclimvarRES,   2)
tabclimvarGEO    = ma.power(tabclimvarGEO,   2)
tabclimvarGEOBTR = ma.power(tabclimvarGEOBTR,2)
#
# 26.46676°N (computation of valormoc)
id26lat    = ma.abs(lat-26.46676).argmin()
id26latBTR = ma.abs(latBTR-26.46676).argmin()
id5N = ma.abs(latBTR-5).argmin()
id5S = ma.abs(latBTR+5).argmin()
id5Nmoc = ma.abs(lat-5).argmin()
id5Smoc = ma.abs(lat+5).argmin()

#
# Chaotic fraction
# =================
tabratio       = ma.divide( tabspread,       tabclimvar      )
tabratioBTR    = ma.divide( tabspreadBTR,    tabclimvarBTR   )
tabratioRES    = ma.divide( tabspreadRES,    tabclimvarRES   )
tabratioGEO    = ma.divide( tabspreadGEO,    tabclimvarGEO   )
tabratioGEOBTR = ma.divide( tabspreadGEOBTR, tabclimvarGEOBTR)
#
# Component
# =========
tabclimmean_box = tabclimmean[(ma.abs(depth+500)).argmin(): (ma.abs(depth+2000)).argmin(),:]
tabratio_box = tabratio[ (ma.abs(depth+500)).argmin(): (ma.abs(depth+2000)).argmin(),:]
id_amoc_max = ma.argmax(tabclimmean_box , axis=0)
fraction = tabratio_box[ id_amoc_max, np.arange(0,3059)]
secdepth = depth[(ma.abs(depth+500)).argmin(): (ma.abs(depth+2000)).argmin()][id_amoc_max]
#
tabratioBTR_box    = tabratioBTR[    (ma.abs(depth+500)).argmin(): (ma.abs(depth+2000)).argmin(),:]
tabratioRES_box    = tabratioRES[    (ma.abs(depth+500)).argmin(): (ma.abs(depth+2000)).argmin(),:]
tabratioGEO_box    = tabratioGEO[    (ma.abs(depth+500)).argmin(): (ma.abs(depth+2000)).argmin(),:]
tabratioGEOBTR_box = tabratioGEOBTR[ (ma.abs(depth+500)).argmin(): (ma.abs(depth+2000)).argmin(),:]
fractionBTR    = tabratioBTR_box[    id_amoc_max[999:999+1800], np.arange(0,1800)]
fractionRES    = tabratioRES_box[    id_amoc_max[999:999+1800], np.arange(0,1800)]
fractionGEO    = tabratioGEO_box[    id_amoc_max[999:999+1800], np.arange(0,1800)]
fractionGEOBTR = tabratioGEOBTR_box[ id_amoc_max[999:999+1800], np.arange(0,1800)]
#
# 
fig = plt.figure(figsize=(8,9), dpi=1000,facecolor='w')
cmapstd  = plt.get_cmap( 'ocean_r', 21)
labels = ['25$^\\circ$S','15$^\\circ$S','5$^\\circ$S','EQ','5$^\\circ$N','15$^\\circ$N','25$^\\circ$N','35$^\\circ$N','45$^\\circ$N','55$^\\circ$N','65$^\\circ$N']
#
fslab=12
fstlab=10
fscbtick=10
#
ax1 = plt.subplot(311)
plt.pcolor(lat,-depth,tabspread,cmap=cmapstd,vmin=0,vmax=15)
plt.axvline(x=26,ymin=0,ymax=6000,color='red',linewidth=1.3)
ax1.add_line(Line2D(lat,secdepth,color='black',lw=1.2))
ti = ax1.set_title('(a) Ensemble spread saturation',fontsize=14)
ax1.set_xticks([-25., -15., -5., 0., 5., 15., 25., 35., 45., 55., 65.])
ax1.set_xticklabels(labels,fontsize=fstlab)
plt.setp(ax1.get_yticklabels(), fontsize=fstlab)
ax1.set_xlim([-34., 65.])
ax1.set_ylim([0., 5700.])
ax1.invert_yaxis()
ax1.set_ylabel('depth (m)',fontsize=fslab)
ax1.set_facecolor('lightgray')
#
# ax1b = ax1.twinx() 
# ax1b.plot(lat,secdepth,color='black',lw=1.3)
# ax1b.set_xlim([-34., 65.])
# divider = make_axes_locatable(ax1b)
# cax1b = divider.append_axes("right", size="5%", pad=0.3)
# cax1b.set_facecolor('none')
# for axis in ['top','bottom','left','right']:
#     cax1b.spines[axis].set_linewidth(0)
# cax1b.set_xticks([])
# cax1b.set_yticks([])
#
# axe pour la colorbar 1
divider = make_axes_locatable(ax1)
cax1 = divider.append_axes("right", size="5%", pad=0.3)
cb = plt.colorbar(cax=cax1)
cb.set_label('Transport variance (Sv$^2$)',fontsize=fslab)
cb.ax.tick_params(labelsize=fscbtick)
##
ax2 = plt.subplot(312)
plt.pcolor(lat,-depth,tabratio,cmap=cmapstd,vmin=0,vmax=+1)
plt.axvline(x=26,ymin=0,ymax=6000,color='red',linewidth=1.3)
ax2.add_line(Line2D(lat,secdepth,color='black',lw=1.2))
ti = ax2.set_title('(b) Chaotic variability fraction',fontsize=14)
ax2.set_xticks([-25., -15., -5., 0., 5., 15., 25., 35., 45., 55., 65.])
ax2.set_xticklabels(labels,fontsize=fstlab)
plt.setp(ax2.get_yticklabels(), fontsize=fstlab)
ax2.set_xlim([-34., 65.])
ax2.set_ylim([0., 5700.])
ax2.invert_yaxis()
ax2.set_ylabel('depth (m)',fontsize=fslab)
ax2.set_facecolor('lightgray')
#
# axe pour la colorbar 1
divider = make_axes_locatable(ax2)
cax2 = divider.append_axes("right", size="5%", pad=0.3)
cb = plt.colorbar(cax=cax2)
cb.set_label('Fraction',fontsize=fslab)
cb.ax.tick_params(labelsize=fscbtick)
#
 
ax3 = plt.subplot(313)
plt.plot( lat,    fraction,       color='red'    ,lw=1.5)
plt.plot( latBTR, fractionBTR,    color='blue'   ,lw=1.2)
plt.plot( latBTR[0:id5S], fractionGEO[0:id5S],    color='fuchsia',lw=1.2)
plt.plot( latBTR[id5N:1800], fractionGEO[id5N:1800], color='fuchsia',lw=1.2)
plt.plot( latBTR[0:id5S], fractionRES[0:id5S],    color='black',lw=1.2)
plt.plot( latBTR[id5N:1800], fractionRES[id5N:1800], color='black',lw=1.2)
plt.plot( latBTR[0:id5S], fractionGEOBTR[0:id5S], color='orange', lw=1.2)
plt.plot( latBTR[id5N:1800], fractionGEOBTR[id5N:1800], color='orange', lw=1.2)
ax3.axvline(x=26,ymin=0,ymax=6000,color='red',linewidth=1.3)
#cb3 = plt.colorbar()
ti = ax3.set_title('(c) Chaotic fraction at AMOC index level',fontsize=14)
ax3.set_xticks([-25., -15., -5., 0., 5., 15., 25., 35., 45., 55., 65.]
)
ax3.set_xticklabels(labels,fontsize=fstlab)
plt.setp(ax3.get_yticklabels(), fontsize=fstlab)
ax3.set_xlim([-34., 65.])
ax3.set_ylim([0., 1.2])
#
# rajout d'un axe vide pour l'alignement des subplots
divider = make_axes_locatable(ax3)
cax3 = divider.append_axes("right", size="5%", pad=0.3)
cax3.set_facecolor('none')
for axis in ['top','bottom','left','right']:
    cax3.spines[axis].set_linewidth(0)
cax3.set_xticks([])
cax3.set_yticks([])
lamoc   = Line2D([], [], color='red',     label=' amoc'   )
lbtr    = Line2D([], [], color='blue',    label=' btr'    )
lres    = Line2D([], [], color='black',   label=' residual'    )
lgeo    = Line2D([], [], color='fuchsia', label=' geosh'    )
lgeobtr = Line2D([], [], color='orange',  label=' geosh+btr')
cax3.legend(handles=[lamoc,lbtr,lgeo,lgeobtr,lres],frameon=False,loc=(-1,0.1),fontsize=10,handletextpad=0.,borderpad=1. )
#leg = plt.legend((lamoc,lbtr,lgeo,lgeobtr),['amoc','btr','geo','geo+btr'])


plt.subplots_adjust(hspace=0.3)
plt.savefig('../figures/figure_06.png')

