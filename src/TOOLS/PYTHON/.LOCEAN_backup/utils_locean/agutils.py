# -*-coding:Latin-1 -*
#======================================================================== 
import netCDF4 as nc
import datetime
# =======================================================================
# Fonction de gestion des netcdf
# ==============================
def read(dirin,filein,varname,years=None) :
  """ tab, timeval, timu, timecal = read(dirin,filein,varname,years=None)

  Lit la variable varname dans le netcdf filein, sur la periode définie dans years.
  """
  try :
    f=nc.Dataset(dirin+filein)
  except :
    """Couldn't find the file %s"""%(dirin+filein)
  #tab = f.variables[varname][0:12,:,:]
  timeaxis = f.variables['time_counter']
  timeu = timeaxis.units
  timecal = timeaxis.calendar
  #
  if years is not None :
    tdeb = datetime.datetime(years[0],1,1) # 1er Jan de la 1ere année
    tfin = datetime.datetime(years[-1],12,31,23,59,00) #31/12 de la dernière année
    ideb = nc.date2index(tdeb,timeaxis,calendar=timeaxis.calendar,select='after')
    ifin = nc.date2index(tfin,timeaxis,calendar=timeaxis.calendar,select='before')
    timeval = timeaxis[ideb:ifin+1]
    tab = f.variables[varname][ideb:ifin+1,:,:]
  else :
    tab = f.variables[varname][:,:,:]
    timeval=timeaxis[:]
  #  
  f.close()
  return tab, timeval, timeu, timecal
# -----------------------------------------------------------------------
def get_mask(domain,grid='ORCA2') :
  if grid is 'ORCA2':
    fgrid='/net/argos/data/parvati/agglod/DATA/IPSLCM/Mask_ORCA2.nc'
  try :
    f = nc.Dataset(fgrid)
  except :
    print """Couldn't find de file : %s"""%(fgrid)
  #
  rmask = f.variables[domain][:,:,:]
  f.close()
  return rmask
# -----------------------------------------------------------------------
def myweights(grid='ORCA2') :
  """ myweights(grid='ORCA2')
      Charge les poids correspondant à la grille grid.
  """
  if grid is 'ORCA2' :
    fgrid='/net/cratos/usr/cratos/varclim/IPSLCM5A/PROD/piControl2/OCE/piControl2_mesh_mask.nc'
  else :
    print """I don't know this grid : %s"""%(grid)
  #
  try :
    f = nc.Dataset(fgrid)
  except :
    print """Couldn't find the file : %s """%(fgrid)
  #
  e1t = f.variables['e1t'][0,:,:]
  e2t = f.variables['e2t'][0,:,:]
  f.close()
  #
  wt = e1t*e2t
  # traite le recouvrement sur les pôles, attention, à adapter si
  # on n'utilise pas une grille de type ORCA
  wt[0,:]  = 0.
  wt[-1,:] = 0.
  wt[:,0]  = 0.
  wt[:,-1] = 0.
  return wt
# 
# -----------------------------------------------------------------------
