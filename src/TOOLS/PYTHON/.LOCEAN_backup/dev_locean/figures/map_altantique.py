#!/usr/bin/env python
# -*-coding:Latin-1 -*
# Created : 2013/12 (A. Germe)
# Version: no 00
# Contour sur l'Atlantique Nord
# =========================================================================
import sys, os
import netCDF4 as nc
import MA
import numpy as N
#
from direxp import *
from pylab import *
import matplotlib.colors as col
from mpl_toolkits.basemap import Basemap
from matplotlib.colors import LogNorm
# =========================================================================
def map(tab):

    monthtitle=["January","February","March","April","May","June","July","August","September","October","November","December"]


    if (depth_level==-1):
        data = ( array ( ncfile.variables[var][time-1,:,:]))
    else:
        data = ( array ( ncfile.variables[var][time-1,depth_level,:,:]))
    ncfile.close()

    # PLOT FIGURE
    fig=figure()
    extent=[min(lons),max(lons),min(lats),max(lats)]

    levels = arange(valeurmin, valeurmax, inter_lev)
    print levels
    data=np.where(data==fil_val,-1e33,data)

    m=imshow(data, interpolation='nearest',extent=extent,cmap=palette,norm=colors.normalize(vmin=valeurmin,vmax=valeurmax))
    palette.set_under('grey', 1.0 )


    v=axis()
    m2=contour(lons,lats,data,levels, colors='black',hold='on',origin='image') #cmap=plt.cm.jet)
    # POUR ECRIRE TEMPERATURE le long du contour
 #   clabel(m2,levels[1::2], fmt = '%2.1f', colors = 'black', fontsize=14, inline=1)
    #clabel(m2,levels, fmt = '%2.1f', colors = 'black', fontsize=14, inline=1)
    axis(v)

    xlabel("Longitude",color='k',size=12,weight='bold')
    ylabel("Latitude",color='k',size=12,weight='bold')
    title(monthtitle[time-1],color='k',size=14,weight='bold')

    cbar = colorbar(m)
    cbar.ax.set_ylabel(labelname,size=12,weight='bold')
    cbar.add_lines(m2)
    fname=output_name
    print fname
    savefig(fname)


# =========================================================================
#                               MAIN
# =========================================================================
dirin='/net/cratos/usr/cratos/varclim/agglod/mydiags/OUTPUTS/Ocean/clim2d/AR5/CTL/'
filein='piControl2_clim2d_sosstsst_1800-2799.nc'

# Read netcdf file
tab,tax,lon,lat = ct.readfield(dirin,filein,varname='clim_sosstsst')


