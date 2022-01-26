# -*-coding:Latin-1-*
# =========================================================================
# Packages de fonctions utilse à l'analyse de données climatiques
#
# Author : A. Germe
# 25 Nov. 2013
# =========================================================================
import sys, os,
import netCDF4 as nc
import datetime
#
import MA
import numpy as N
#
from direxp import *
# =========================================================================
# =========================================================================
# Fonctions de lectures 
# ----------------------
def read(dirin,filein,varname,years=None) :
  try :
    f=nc.Dataset(dirin+filein)
  except :
    """Couldn't find the file %s"""%(dirin+filein)
  tab = f.variables[varname][0:12,:,:]
  timeaxis = f.variables['time_counter']
  timeu = timeaxis.units
  #
  if years is not None :
    tdeb = datetime.datetime(years[0],1,1) # 1er Jan de la 1ere année
    tfin = datetime.datetime(years[-1],12,31) #31/12 de la dernière année
    ideb = nc.date2index(tdeb,timeaxis,calendar=timeaxis.calendar,select='after')
    ifin = nc.date2index(tfin,timeaxis,calendar=timeaxis.calendar,select='before')
    timeval = timeaxis[ideb:ifin+1]
    tab = f.variables[varname][ideb:ifin+1,:,:]
  else :
    tab = f.variables[varname][:,:,:]
    timeval=timeaxis[:]
  #  
  f.close()
  return tab, timeval, timeu
# ----------------------
def readfield(dirin,filein,varname,years=None) :
  try :
    f=nc.Dataset(dirin+filein)
  except :
    """Couldn't find the file %s"""%(dirin+filein)
  timeaxis = f.variables['time_counter']
  timeu = timeaxis.units
  lon = f.variables['nav_lon']
  lat = f.variables['nav_lat']
  #
  if years is not None :
    tdeb = datetime.datetime(years[0],1,1) # 1er Jan de la 1ere année
    tfin = datetime.datetime(years[-1],12,31) #31/12 de la dernière année
    ideb = nc.date2index(tdeb,timeaxis,calendar=timeaxis.calendar,select='after')
    ifin = nc.date2index(tfin,timeaxis,calendar=timeaxis.calendar,select='before')
    timeval = timeaxis[ideb:ifin+1]
    tab = f.variables[varname][ideb:ifin+1,:,:]
  else :
    tab = f.variables[varname][:,:,:]
    timeval=timeaxis[:]
  #  
  f.close()
  return tab, lon, lat, timeax
# =========================================================================
# =========================================================================
class timeaxis :
    """ Objet perso qui definie un axe des temps associé à un champ ou serie
    temporelle.
    Il s'agit en fait d'une array numpy contenant des objets de type classtime, à laquelle j'ai associé qques méthode

    Method disponible
    """
    def __init__(self,values,units,calendar='noleap',origin=None) :
        self.values=values
        self.units=units
        self.calendar=calendar
        self.origin=origin
    #
    # -----------------------------------------------------
    def list(self) :
        """ timeax.list()
        Liste les caractéristiques de l'axe des temps timeax
        """
        print "Caracteristics :"
        print "shape : " shape(self.values)
        print "units : " self.units
        print "Calendar : " self.calendar
        if origin is not None : print "origin : " self.origin
    #
    # -----------------------------------------------------
    def month(self) :
        months = N.array(list(elt.month for elt in self.values))
        return months
    #
    # -----------------------------------------------------
    def year(self) : 
        years = N.array(list(elt.year for elt in self.values))
    #
    # -----------------------------------------------------
    def day(self) : 
        years = N.array(list(elt.day for elt in self.values))
    #
    # -----------------------------------------------------
    def dayofwk(self) : 
        years = N.array(list(elt.day for elt in self.values))
    #
    # -----------------------------------------------------
    def dayofyr(self) : 
        years = N.array(list(elt.day for elt in self.values))
    #
    # -----------------------------------------------------
    def 2num(self) :
        nc.date2num(self.values)
    #
    # -----------------------------------------------------

# Timeseries:
# -----------
def selectmth(tab,time,timeu,timepos=0) :
    timeax = nc.num2date(time, units=timeu, calendar='noleap')


# =========================================================================
# =========================================================================
# Moyenne et clim
# ----------------
def clim2d(expid,variable,period=None,season='ALL',mod='I') :
    """ Calcule et enregistre dans un netcdf la moyenne, l'ecart-type et la tendance d'un champs suivant la dimension time.

        clim2d(expid,varname,season='ALL',period=None,mod='I')

        INPUT :
        expid --> str: identifant de l'experience
        varname --> str: nom de la variable
        season --> str: saison, les saisons connues sont celles de la fonction GEN.read d'Aurore
        period --> list: annÃ©es sur lesquelles on fait le calcule
        mod --> str: realm

        OUPUT :
        Pas d'output dans le workspace, mais creation d'un netcdf contenant :
        clim --> MV.array : Moyenne temporelle du champs
        std --> MV.array : Ecart-type temporel du champs
        trend --> MV.arrayn : tendance linaire du champs
        pval --> p-value associÃ©e au trend

        FILE :
        Le fichier de sorti se trouve dans un sous repertoire de :
        '/home/germe/mydiags/OUTPUT/'
        Le sous repertoire est fonction de l'experience, et du realm.
    """
    #
    exp = dexp[expid]
    # repertoire des sorties :
    climout='/net/cratos/usr/cratos/varclim/agglod/mydiags/OUTPUTS/'
    if mod is 'I' : ssrep='SeaIce/clim2d'
    if mod is 'A' : ssrep='Atmo/clim2d'
    if mod is 'O' : ssrep='Ocean/clim2d'
    try :
        climout = climout+ssrep
    except :
        print """There is no realm %s for the expe %S"""%(mod,expid)
    if exp.ismember :
        dirout = '%s/%s/%s/%s/'%(climout,exp.stream,exp.group,exp.ensemblename)
    else :
        dirout = '%s/%s/%s/'%(climout,exp.stream,exp.group)

    if not os.path.exists(dirout) : os.makedirs(dirout)

    # fichier de sortie
    fileout = '%s%s_clim2d_%s_%i-%i.nc'%(dirout,expid,varname,period[0],period[1])
    print """OUTPUTS will be placed in %s"""%(fileout)
    datefile = datetime.date.today() 
    fileo = nc.Dataset(fileout,'w')
    fileo.date = str(datefile)
    fileo.code = 'climtools/clim2d'
    fileo.author = 'A. Germe'
    fileo.period = str(period[0])+'-'+str(period[-1])
    fileo.expid = expid

    # Inputs
    dirin  = exp.loc(mod)
    filein = exp.fname(varname)

    field, lon, lat, timeval, timeu = readfield(dirin,filein,varname,years=period)
    # check si le nombre d'annÃ©es correspond Ã  la demande
    #Nyr = period[-1] - period[0]+1
    #years  = MV.array(list(elt.year  for elt in ))
    #listyears = list(set(years)) # une maniÃ¨re d'enlever les doublons    
    #if not len(listyears)==Nyr :
    #    print """Warning : Number of years avaiblable is not in accordance with the chosen period"""
    newshape = (12,)+field.shape[1:])
    clim = N.empty(newshape)
    std = N.empty(newshape)
    trend = N.empty(newshape)
    pval = N.empty(newshape)
    if len(timeval) !=1 :
        clim = U.averager(field,axis='t')
        std  = S.std(field,axis='t')
        trend, pval = S.linearregression(field,axis='t',nointercept=1,error=1)
        #
        fileo.write(clim, id='clim_'+variable)
        fileo.write(std, id='std_'+variable)
        fileo.write(trend, id='trend_'+variable)
        fileo.write(pval, id='pval_'+variable)
    else :
        clim=field
        std=N.zeros(field.shape)
        trend=N.zeros(field.shape)
        pval=None
        #
        clim.setAxisList(axes[1:])
        std.setAxisList(axes[1:])
        trend.setAxisList(axes[1:])
        #
        clim.setGrid(grid)
        std.setGrid(grid)
        trend.setGrid(grid)
        #
        fileo.write(clim, id='clim_'+variable)
        fileo.write(std, id='std_'+variable)
        fileo.write(trend, id='trend_'+variable)
    #
    #
    fileo.close()
#
# ---------------------------------------------------------------------------
#




