# -*-coding:Latin-1 -*
# -*- coding:UTF-8 -*- 
#!/usr/bin/env cdat
# ==============================================================================
import netCDF4 as nc
import MA
import numpy as N 
import datetime
import sys, os
#
from direxp import *
import agutils as ag
import climtools as ct
# ===========================================================================
#  utilisation :
# cdat -i calc_PWfluw_monthly_Fram.py EXP_ID
# Exemple :
#        cdat -i calc_PWfluw_monthly_Fram.py HISTNUD15 
# =======================================================================
# Utile pour la lecture :
# ========================
#
# moce : Masque de l'ocÃ©an
#       --> array dans laquelle, 0=Land, 1=Ocean, 2= Section d'intÃ©ret
#
# l : Definition de la section 
#     -->LISTE Contenant les indices des mailles de la section d'intÃ©ret en
#        grille NEMO1
#
# sec : mÃªme chose que l, mais sous forme d'array de dimension (N,2),
#       avec N le nombre de maille dans la section
#
# extr : fonction qui extrait la section d'intÃ©ret d'un champs 3D (Nx,Ny,Nz)
#        d'un input de dim (Nt,Nz,Ny,Nx) ressort
#        un output de dim (Nt,N,Nz) N=Nbe de mailles de sec
#        ==> ressort des sections verticales
#
# extr2D : mÃªme chose pour champs 2D (Ny,Nx)
#
# re1v : Contient la dimension dx de la maille, pour chaque maille de
#        la section d'interet (grille V)
# re2u : Contient la dimension dy de la maille, pour chaque maille de
#        la section d'intÃ©ret (grille U)
#
# nlev : Contient les profondeurs z (en m) des niveaux de la grille
#        dim=(42), 42 niveaux
#
# o1 : Contient la diffÃ©rence d'indice en x et en y d'une maille Ã  l'autre
#      dans la section d'intÃ©ret. dim (N,2)
#      Dans le cas de Fram, cette section est zonale, i.e. suivant un indice
#      constant i=271
#      Alors o1[:,0]=0
#      Et on prend toutes les mailles d'affiler sur un mÃªme parallÃ¨ne
#      Alors o1[:,1]=1
#      Rq : dans le cas d'une section plus complexe on ferait N.diff(sec)
#
# oo3D : MÃªme chose rÃ©pliquÃ© sur les 42 niveaux verticaux
#        Sert au calcule du transport.
#        En effet : sur une maille, le dÃ©bit zonale : u*dy est Ã  prendre
#        en compte
#           positivement si la maille en i+1 a pour indice y-1
#           negativement si la maille en i+1 a pour indice y+1
#           zero         si al maille en i+1 a pour indice y  
# =========================================================================
# Some functions
# ==============
#def years(filein) :
#  info=filein.split('_')
#  yrdeb=int(info[1][0:4])
#  yrfin=int(info[2][0:4])
#  return [yrdeb,yrfin]
# -----------------------------------------------------------------------
def read(dirin,filein,varname,years=None) :
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
  return tab, timeval, timeu, timecal
# =======================================================================
# Function d'extraction d'une section
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def extr(champ,listij):
 if len(champ.shape)>3:
  Nt = champ.shape[0]
  res=N.zeros([Nt,listij.shape[0],31])
  for ip in range(listij.shape[0]):
   ipi=listij[ip,0]
   ipj=listij[ip,1]
   res[:,ip,:]=champ[:,:,ipi,ipj]
 else:
  res=N.zeros([listij.shape[0],31])
  for ip in range(listij.shape[0]):
   ipi=listij[ip,0]
   ipj=listij[ip,1]
   res[ip,:]=champ[:,ipi,ipj]
 #
 return res
 # --> dim(res) = (Npoints de la section, Nlevel=42)
#
def extr2D(champ,listij):
 if len(champ.shape)>2:
  Nt = champ.shape[0]
  res=N.zeros([Nt,listij.shape[0]])
  for ip in range(listij.shape[0]):
   ipi=listij[ip,0]
   ipj=listij[ip,1]
   res[:,ip]=champ[:,ipi,ipj]
 else:
  res=N.zeros([listij.shape[0]])
  for ip in range(listij.shape[0]):
   ipi=listij[ip,0]
   ipj=listij[ip,1]
   res[ip]=champ[ipi,ipj]
 #
 return res
 # --> dim(res) = (Npoints de la section)
#
# =======================================================================
EXP_ID = sys.argv[1]
if len(sys.argv)<3 :
  fin = None
else :
  fin = sys.argv[2]
#
DIAG_ID = 'SIflux_Fram_sic'

# Experience
# ~~~~~~~~~~~~~~~~~~~~~~~
exp = dexp[EXP_ID]

# Repertoires des outputs :
# ~~~~~~~~~~~~~~~~~~~~~~~~~
if exp.ismember :
  dirout = '/net/cratos/usr/cratos/varclim/agglod/mydiags/OUTPUTS/SeaIce/%s/%s/%s/'%(exp.stream,exp.group,exp.ensemblename)
else :
  dirout = '/net/cratos/usr/cratos/varclim/agglod/mydiags/OUTPUTS/SeaIce/%s/%s/'%(exp.stream,exp.group)
fileout = '%s%s_%s.nc'%(dirout,EXP_ID,DIAG_ID)


# annÃ©es disponibles
# ~~~~~~~~~~~~~~~~~~~
[yrdeb, yrfin] = exp.year
print('Dates available for %s : %i-%i'%(EXP_ID,yrdeb,yrfin))
if fin is not None :
  yrfin=int(fin)
  print('To your request, the computation will stop for yrfin = %s'%(fin))

# =========================================================================
# Definition des sections
# ~~~~~~~~~~~~~~~~~~~~~~~
moce=ag.get_mask('GLOOCEAN')[0]
moce[136,131:140]=2.

fram = ag.get_mask('FRAMSTRX')[0]
frami = fram.nonzero()
l = zip(frami[0],frami[1])
sec = N.array(l)
#
# Valeurs utiles pour le calcule de transport
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# taille des mailles
f=nc.Dataset('/net/cratos/usr/cratos/varclim/IPSLCM5A/PROD/piControl2/OCE/piControl2_mesh_mask.nc')
e1v=f.variables['e1v'][0]
e2u=f.variables['e2u'][0]
f.close()
#
e1v3D=N.repeat(N.reshape(e1v,(1,)+e1v.shape),31,axis=0)
e2u3D=N.repeat(N.reshape(e2u,(1,)+e2u.shape),31,axis=0)
re1v=extr(e1v3D,sec)
re2u=extr(e2u3D,sec)
re1v = N.rollaxis(re1v,1)
re2u = N.rollaxis(re2u,1)
#
o1=N.zeros([sec.shape[0],2])
o1[:,0]=0.
o1[:,1]=1.
#
oo3D=N.repeat(N.reshape(o1,(1,)+o1.shape),31,axis=0)
#

# ========================================================================
# Main routine
# ========================================================================
if not os.path.exists(dirout) : os.makedirs(dirout)
#
if os.path.exists(fileout) :
  fileo = nc.Dataset(fileout,'a')
  framivt = fileo.variables['FRAMivt']
  framiat = fileo.variables['FRAMiat']
  times = fileo.variables['time_counter']
  if 'FRAMivt' in fileo.variables.keys() :
    last_year_done = nc.num2date(times[-1],times.units).year
    last_year_to_do = yrfin
    yrdeb = last_year_done+1
    if fin is not None :
      last_year_to_do=int(fin)
    print last_year_done+1, last_year_to_do+1
else :
  datefile = datetime.date.today() 
  fileo = nc.Dataset(fileout,'w')
  fileo.date = str(datefile)
  fileo.author = 'A. Germe'
  fileo.comment = 'Par rapport au diag SIflux_Fram, cette version prend en compte la pondération par la fraction de glace pour le calcule du flux de volume. C\'est à dire que h est prix égale à iicethic*soicecov, de manière à considérer une épaisseur moyenne sur toute la maille. En d\'autres termes, on considère que l volume est homogénement réparti sur la maille. Pour FRAMiat, identique au diag précédent, sans pris en compte de la sea ice fraction, on a juste u*dy+v*dx.'
  time = fileo.createDimension('time',None)
  times = fileo.createVariable('time_counter','f',('time',))
  framivt = fileo.createVariable('FRAMivt','f',('time',))
  framiat = fileo.createVariable('FRAMiat','f',('time',))
  framivt.units='km3'
  framiat.units='km2'
  framivt.long_name = "Fram Strait sea ice volume transport"
  framiat.long_name = "Fram Strait sea ice area transport"
#
#
for year in range(yrdeb,yrfin+1):
 #
 print """computing year %i"""%(year)
 #
 ui, timex = ct.read(exp.locfile('iicevelu',realm='I'),'iicevelu',years=range(year,year+1))
 uui = extr2D(ui,sec)
 #
 vi,timex = ct.read(exp.locfile('iicevelv',realm='I'),'iicevelv',years=range(year,year+1))
 vvi = extr2D(vi,sec)
 #
 hi,timex = ct.read(exp.locfile('iicethic',realm='I'),'iicethic',years=range(year,year+1))
 hhi = extr2D(hi,sec)
 #
 ai,timex = ct.read(exp.locfile('soicecov',realm='I'),'soicecov',years=range(year,year+1))
 aai = extr2D(ai,sec)
 #

 print "loading done, computing ..."
 for mth in range(12):
  print mth+1
  tmpui=uui[mth]
  tmpvi=vvi[mth]
  tmphi=hhi[mth]
  tmpai=aai[mth]
  fvi=((tmpui*oo3D[0,:,0]*re2u[0,:] + tmpvi*oo3D[0,:,1]*re1v[0,:])*tmphi*tmpai).sum()
  fai=((tmpui*oo3D[0,:,0]*re2u[0,:] + tmpvi*oo3D[0,:,1]*re1v[0,:])).sum()
  #
  # Transport cumulé sur le mois en km3 et km2  respectivement:
  if mth<11 :
    delta = datetime.datetime(year,mth+2,01,00,00,00) - datetime.datetime(year,mth+1,01,00,00,00)
  else :
    delta = datetime.datetime(year+1,01,01,00,00,00) - datetime.datetime(year,mth+1,01,00,00,00)
  fvic = fvi*delta.days*3600*1e-9
  faic = fai*delta.days*3600*1e-6
  #
  #
  if framivt.shape[0]==0 :
    framivt[0] = fvic
    framiat[0] = faic
    times[0] = timex.num()[mth]
  else :
    i1=len(framivt)
    framivt[i1] = fvic
    framiat[i1] = faic
    times[i1] = timex.num()[mth]
  #

times.calendar = timex.calendar
times.units = timex.units
fileo.close()




