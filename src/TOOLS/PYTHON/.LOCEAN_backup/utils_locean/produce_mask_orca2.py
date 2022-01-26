#!/usr/bin/env cdat
# -*-coding:Latin-1 -*
# ==========================================================================
import sys
import netCDF4 as nc
import MA
import numpy as N
import datetime
# ==========================================================================
#
option_grid = 't'
fmask = nc.Dataset('/net/cratos/usr/cratos/varclim/IPSLCM5A/PROD/piControl2/OCE/piControl2_mesh_mask.nc')
mask_v = fmask.variables[option_grid + 'mask'][0]
longitude = fmask.variables['nav_lon'][:,:]
latitude  = fmask.variables['nav_lat'][:,:]
level = fmask.variables['nav_lev'][:]
fmask.close()
#
dom_dict2d = dict()
dom_dict = dict()
lname_dict = dict()
dom_arct = dict()
dom_arct2d = dict()
#dom_name = dict()
#
#GENERAL SEA AREAS
#
#Global ocean
dom_dict['GLOOCEAN'] = mask_v
lname_dict['GLOOCEAN'] = 'Global Ocean'
#
# Global Ocean in between 60S-60N
glo60 = N.where(N.logical_and(latitude>-60,latitude<60),mask_v,0)
dom_dict['GLOOCEAN60'] = glo60
lname_dict['GLOOCEAN60'] = 'Global Ocean in between 60S-60N' 
#
#North Hemisphere
nhemisph = N.where(latitude > 0,mask_v,0)
dom_dict['NHEMISPH'] = nhemisph
lname_dict['NHEMISPH'] = 'Northern Hemisphere'
#
#South Hemisphere
shemisph = N.where(latitude < 0,mask_v,0)
dom_dict['SHEMISPH'] = shemisph
lname_dict['SHEMISPH'] = 'Southern Hemisphere'
#
#Antarctic Ocean
antarctx = N.where(latitude < -50.,mask_v,0)
dom_dict['ANTARCTX'] = antarctx
lname_dict['ANTARCTX'] = 'Antarctic Ocean'
#
# bande équatorial
bool_trop20 = N.logical_and(latitude<20,latitude>-20)
trop20 = N.where(bool_trop20,mask_v,0)
dom_dict['TROP20'] = trop20
lname_dict['TROP20'] = 'Tropics (equatorial band toward 20N and S)'
#
# bande équatorial
bool_trop10 = N.logical_and(latitude<10,latitude>-10)
trop10 = N.where(bool_trop10,mask_v,0)
dom_dict['TROP10'] = trop10
lname_dict['TROP10'] = 'Equatorial band toward 10N and S)'


#Northern Northern Hemisphere
#nnhemisph = 
#
#Mediterranean Sea
bool_medit_1 = N.logical_and(N.logical_and(latitude > 30,latitude < 40), N.logical_and(longitude>-5, longitude <0))
bool_medit_2 = N.logical_and(N.logical_and(latitude > 30,latitude < 46), N.logical_and(longitude > 0, longitude <28))
bool_medit_3 = N.logical_and(N.logical_and(latitude > 30,latitude < 40), N.logical_and(longitude > 28, longitude <40))
bool_medit = N.logical_or(N.logical_or(bool_medit_1,bool_medit_2),bool_medit_3)
mediterr = N.where(bool_medit, mask_v, 0)
dom_dict['MEDITERR'] = mediterr
lname_dict['MEDITERR'] = 'Mediterranean Sea'
#
#Baltic Sea
#bool_baltic = N.
#
#North Atlantic
bool_natl_1 = N.logical_and(N.logical_and(latitude > 32,latitude < 73), N.logical_and(longitude>-95, longitude <26))
bool_natl_2 = N.logical_and(N.logical_and(latitude > 73,latitude < 75), N.logical_and(longitude>-30, longitude <24))
bool_natl_3 = N.logical_and(N.logical_and(latitude > 75,latitude < 77), N.logical_and(longitude>-30, longitude <22))
bool_natl_4 = N.logical_and(N.logical_and(latitude > 77,latitude < 79), N.logical_and(longitude>-30, longitude <18))
#Fram Strait!!!
bool_natl_5 = N.logical_and(N.logical_and(latitude > 79,latitude < 81), N.logical_and(longitude>-30, longitude <17))
#
bool_natl_6 = N.logical_and(N.logical_and(latitude > 73,latitude <= 82), N.logical_and(longitude>-83, longitude <-35))
bool_natl = N.logical_or(N.logical_or(bool_natl_1,bool_natl_2),bool_natl_3)
bool_natl = N.logical_or(bool_natl,bool_natl_4)
bool_natl = N.logical_or(bool_natl,bool_natl_5)
bool_natl = N.logical_or(bool_natl,bool_natl_6)
bool_natl = N.logical_and(bool_natl,N.logical_not(bool_medit))
northatl = N.where(bool_natl,mask_v,0)
dom_dict['NORTHATL'] = northatl
lname_dict['NORTHATL'] = 'North Atlantic'
#
#
#Atlantic Ocean
#---------------
bool_atl_1 = N.logical_and(N.logical_and(latitude>6 ,latitude < 73), N.logical_and(longitude>-99,longitude <26)) 
bool_atl_2 = N.logical_and(N.logical_and(latitude>-90 ,latitude<6),N.logical_and(longitude>-72,longitude<22))
bool_atl_3 = N.logical_or(N.logical_or(latitude<3,latitude>7.5),N.logical_or(longitude<-93,longitude>-74)) 
bool_atl_4 = N.logical_or(N.logical_or(latitude<5,latitude>13),N.logical_or(longitude<-97,longitude>-84)) 
bool_atl_5 = N.logical_or(N.logical_or(latitude<5,latitude>16),N.logical_or(longitude<-100,longitude>-88.5)) 
bool_atl_6 = N.logical_or(N.logical_or(latitude<40,latitude>49),N.logical_or(longitude<-96, longitude>-73.5)) # pour virer les lacs
#
bool_atl = N.logical_or(N.logical_or(bool_atl_1,bool_natl_2),bool_natl_3)
bool_atl = N.logical_or(bool_atl,bool_natl_4)
bool_atl = N.logical_or(bool_atl,bool_natl_5)
bool_atl = N.logical_or(bool_atl,bool_natl_6)
bool_atl = N.logical_or(bool_atl,bool_atl_2)
bool_atl = N.logical_and(bool_atl,bool_atl_3)
bool_atl = N.logical_and(bool_atl,bool_atl_4)
bool_atl = N.logical_and(bool_atl,bool_atl_5)
bool_atl = N.logical_and(bool_atl,bool_atl_6)
#
# with mediterranean
atlmed = N.where(bool_atl,mask_v,0)
dom_dict['ATLMED'] = atlmed
lname_dict['ATLMED'] = 'Atlantic Ocean with Mediterranean sea included'
#
# Atlantic tropical
bool_atltrop20 = N.logical_and(bool_trop20,bool_atl)
atltrop20 = N.where(bool_atltrop20,mask_v,0)
dom_dict['ATLTROP20'] = atltrop20
lname_dict['ATLTROP20'] = 'Atlantic Ocean tropical band (20N and S)'

# Atlantic equatorial
bool_atltrop10 = N.logical_and(bool_trop10,bool_atl)
atltrop10 = N.where(bool_atltrop10,mask_v,0)
dom_dict['ATLTROP10'] = atltrop10
lname_dict['ATLTROP10'] = 'Atlantic Ocean equatorial band 10N and S)'
#

# Altantic sud
bool_atlsouth0 = N.logical_and(bool_atl,latitude<0)
atlsouth0 = N.where(bool_atlsouth0,mask_v,0)
dom_dict['ATLSOUTH0'] = atlsouth0
lname_dict['ATLSOUTH0'] = 'Atlantic Ocean south of 0S)'

# Altantic sud
bool_atlsouth10 = N.logical_and(bool_atl,latitude<-10)
atlsouth10 = N.where(bool_atlsouth10,mask_v,0)
dom_dict['ATLSOUTH10'] = atlsouth10
lname_dict['ATLSOUTH10'] = 'Atlantic Ocean south of 10S)'

# Altantic sud
bool_atlsouth20 = N.logical_and(bool_atl,latitude<-20)
atlsouth20 = N.where(bool_atlsouth20,mask_v,0)
dom_dict['ATLSOUTH20'] = atlsouth20
lname_dict['ATLSOUTH20'] = 'Atlantic Ocean south of 20S)'

# Altantic sud
bool_atlsouth30 = N.logical_and(bool_atl,latitude<-30)
atlsouth30 = N.where(bool_atlsouth30,mask_v,0)
dom_dict['ATLSOUTH30'] = atlsouth30
lname_dict['ATLSOUTH30'] = 'Atlantic Ocean south of 30S)'

# Altantic sud
bool_atlsouth40 = N.logical_and(bool_atl,latitude<-40)
atlsouth40 = N.where(bool_atlsouth40,mask_v,0)
dom_dict['ATLSOUTH40'] = atlsouth40
lname_dict['ATLSOUTH40'] = 'Atlantic Ocean south of 40S)'

# Altantic sud
bool_atlsouth50 = N.logical_and(bool_atl,latitude<-50)
atlsouth50 = N.where(bool_atlsouth50,mask_v,0)
dom_dict['ATLSOUTH50'] = atlsouth50
lname_dict['ATLSOUTH50'] = 'Atlantic Ocean south of 50S)'


# without mediterranean
# ---------------------
bool_atl = N.logical_and(bool_atl,N.logical_not(bool_medit))
atlantic = N.where(bool_atl,mask_v,0)
dom_dict['ATLANTIC'] = atlantic
lname_dict['ATLANTIC'] = 'Atlantic Ocean'

# AMO box domain == atlantic in between 0-60N
bool_amo = N.logical_and(N.logical_and(longitude>-80,longitude<0),N.logical_and(latitude>0,latitude<60))
amobox = N.where(bool_amo,mask_v,0)
dom_dict['AMO'] = amobox
lname_dict['AMO'] = 'Atlantic Multidecadal Oscillation index domain'

# Atlantic 20-70N
bool_atl2070N = N.logical_and(bool_atl,N.logical_and(latitude>20,latitude<70))
atl2070N = N.where(bool_atl2070N,mask_v,0)
dom_dict['ATL2070N'] = atl2070N
lname_dict['ATL2070N'] = 'Atlantic Ocean  20-70N latitudinal band'

# Atlantic 30-70N
bool_atl3070N = N.logical_and(bool_atl,N.logical_and(latitude>30,latitude<70))
atl3070N = N.where(bool_atl3070N,mask_v,0)
dom_dict['ATL3070N'] = atl3070N
lname_dict['ATL3070N'] = 'Atlantic Ocean  30-70N latitudinal band'

# Atlantic 40-70N
bool_atl4070N = N.logical_and(bool_atl,N.logical_and(latitude>40,latitude<70))
atl4070N = N.where(bool_atl4070N,mask_v,0)
dom_dict['ATL4070N'] = atl4070N
lname_dict['ATL4070N'] = 'Atlantic Ocean  40-70N latitudinal band'

# Altantique bande 50-70N
bool_5070N = N.logical_and(latitude>50,latitude<70)
bool_atl5070N = N.logical_and(bool_atl,bool_5070N)
atl5070N = N.where(bool_atl5070N,mask_v,0)
dom_dict['ATL5070N'] = atl5070N
lname_dict['ATL5070N'] = 'Atlantic Ocean in 50-70N zonal band)'

# Altantique bande 0-10
bool_0010N = N.logical_and(latitude>0,latitude<10)
bool_atl0010N = N.logical_and(bool_atl,bool_0010N)
atl0010N = N.where(bool_atl0010N,mask_v,0)
dom_dict['ATL0010N'] = atl0010N
lname_dict['ATL0010N'] = 'Atlantic Ocean in 0-10N zonal band)'

# Altantique bande 0-30
bool_0030N = N.logical_and(latitude>0,latitude<30)
bool_atl0030N = N.logical_and(bool_atl,bool_0030N)
atl0030N = N.where(bool_atl0030N,mask_v,0)
dom_dict['ATL0030N'] = atl0030N
lname_dict['ATL0030N'] = 'Atlantic Ocean in 0-30N zonal band)'

# Altantique bande 10-20N
bool_1020N = N.logical_and(latitude>10,latitude<20)
bool_atl1020N = N.logical_and(bool_atl,bool_1020N)
atl1020N = N.where(bool_atl1020N,mask_v,0)
dom_dict['ATL1020N'] = atl1020N
lname_dict['ATL1020N'] = 'Atlantic Ocean in 10-20N zonal band)'

# Altantique bande 20-30N
bool_2030N = N.logical_and(latitude>20,latitude<30)
bool_atl2030N = N.logical_and(bool_atl,bool_2030N)
atl2030N = N.where(bool_atl2030N,mask_v,0)
dom_dict['ATL2030N'] = atl2030N
lname_dict['ATL2030N'] = 'Atlantic Ocean in 20-30N zonal band)'

# Altantique bande 30-40N
bool_3040N = N.logical_and(latitude>30,latitude<40)
bool_atl3040N = N.logical_and(bool_atl,bool_3040N)
atl3040N = N.where(bool_atl3040N,mask_v,0)
dom_dict['ATL3040N'] = atl3040N
lname_dict['ATL3040N'] = 'Atlantic Ocean in 30-40N zonal band)'

# Altantique bande 40-50N
bool_4050N = N.logical_and(latitude>40,latitude<50)
bool_atl4050N = N.logical_and(bool_atl,bool_4050N)
atl4050N = N.where(bool_atl4050N,mask_v,0)
dom_dict['ATL4050N'] = atl4050N
lname_dict['ATL4050N'] = 'Atlantic Ocean in 40-50N zonal band)'

# Altantique bande 50-60N
bool_5060N = N.logical_and(latitude>50,latitude<60)
bool_atl5060N = N.logical_and(bool_atl,bool_5060N)
atl5060N = N.where(bool_atl5060N,mask_v,0)
dom_dict['ATL5060N'] = atl5060N
lname_dict['ATL5060N'] = 'Atlantic Ocean in 50-60N zonal band)'






#Greenland Sea
bool_green_1 = N.logical_and(N.logical_and(latitude > 76,latitude < 81), N.logical_and(longitude>-30, longitude <17))
bool_green_2 = N.logical_and(N.logical_and(latitude > 75,latitude < 76), N.logical_and(longitude>-30, longitude <12))
bool_green_3 = N.logical_and(N.logical_and(latitude > 74,latitude < 75), N.logical_and(longitude>-30, longitude <9))
bool_green_4 = N.logical_and(N.logical_and(latitude > 73,latitude < 74), N.logical_and(longitude>-30, longitude <4))
bool_green_5 = N.logical_and(N.logical_and(latitude > 72,latitude < 73), N.logical_and(longitude>-30, longitude <0))
bool_green_6 = N.logical_and(N.logical_and(latitude > 71,latitude < 72), N.logical_and(longitude>-30, longitude <-3))
bool_green_7 = N.logical_and(N.logical_and(latitude > 70,latitude < 71), N.logical_and(longitude>-30, longitude <-8))
bool_green = bool_green_1
for i in range(2,8):
 exec('bool_green = N.logical_or(bool_green,bool_green_'+ str(i) +')')

#
greenlan = N.where(bool_green,mask_v,0)
dom_dict['GREENLAN'] = greenlan
lname_dict['GREENLAN'] = 'Greenland Sea'
#
#Icelandic Sea: N->S, Jan Mayen is SE corner
bool_icel_1 = N.logical_and(N.logical_and(latitude > 69,latitude < 70), N.logical_and(longitude>-29, longitude <-9))
bool_icel_2 = N.logical_and(N.logical_and(latitude > 68,latitude < 69), N.logical_and(longitude>-28, longitude <-10))
bool_icel_3 = N.logical_and(N.logical_and(latitude > 67,latitude < 68), N.logical_and(longitude>-25, longitude <-11))
bool_icel_4 = N.logical_and(N.logical_and(latitude > 66,latitude < 67), N.logical_and(longitude>-23, longitude <-12))
bool_icel_5 = N.logical_and(N.logical_and(latitude > 65,latitude < 66), N.logical_and(longitude>-20, longitude <-13))
bool_icel = bool_icel_1 
for i in range(2,6):
 exec('bool_icel=N.logical_or(bool_icel,bool_icel_'+ str(i) +')')

icelands = N.where(bool_icel,mask_v,0)
dom_dict['ICELANDS'] = icelands
lname_dict['ICELANDS'] = 'Icelandic Sea'
#
#Norwegian Sea: N->S, Bjornoya is E corner, then North Cape
bool_norw_1 = N.logical_and(N.logical_and(latitude > 75,latitude < 76), N.logical_and(longitude>12, longitude <17))
bool_norw_2 = N.logical_and(N.logical_and(latitude > 74,latitude < 75), N.logical_and(longitude>9, longitude <18))
bool_norw_3 = N.logical_and(N.logical_and(latitude > 73,latitude < 74), N.logical_and(longitude>4, longitude <19))
#I reached Bjornoya
bool_norw_4 = N.logical_and(N.logical_and(latitude > 72,latitude < 73), N.logical_and(longitude>0, longitude <21))
bool_norw_5 = N.logical_and(N.logical_and(latitude > 71,latitude < 72), N.logical_and(longitude>-3, longitude <23))
bool_norw_6 = N.logical_and(N.logical_and(latitude > 70,latitude < 71), N.logical_and(longitude>-8, longitude <25))
#I reached North Cape
bool_norw_7 = N.logical_and(N.logical_and(latitude > 66,latitude < 70), N.logical_and(longitude>-13, longitude <25))
bool_norw_7 = N.logical_and(bool_norw_7, N.logical_not(bool_icel))
bool_norw_8 = N.logical_and(N.logical_and(latitude > 62,latitude < 66), N.logical_and(longitude>-6, longitude <15))
bool_norw_9 = N.logical_and(N.logical_and(latitude > 61,latitude < 62), N.logical_and(longitude>0, longitude <15))
bool_norw_10 = N.logical_and(N.logical_and(latitude > 63,latitude < 64), N.logical_and(longitude>-8, longitude <-6))
bool_norw_11 = N.logical_and(N.logical_and(latitude > 64,latitude < 65), N.logical_and(longitude>-10, longitude <-6))
bool_norw_12 = N.logical_and(N.logical_and(latitude > 65,latitude < 66), N.logical_and(longitude>-13, longitude <-6))
bool_norw = bool_norw_1
for i in range(2,13):
 exec('bool_norw=N.logical_or(bool_norw,bool_norw_'+ str(i) +')')

norskhav = N.where(bool_norw,mask_v,0)
dom_dict['NORSKHAV'] = norskhav
lname_dict['NORSKHAV'] = 'Norwegian Sea'
#
#GIN seas: simple one!!!
bool_gins = N.logical_or(N.logical_or(bool_green,bool_icel),bool_norw)
ginseasx = N.where(bool_gins,mask_v,0)
dom_dict['GINSEASX'] = ginseasx
dom_arct['GINSEASX'] = ginseasx
lname_dict['GINSEASX'] = 'GIN Seas'
#
#
#Barents Sea (including White Sea)
#E limit of Greenland Sea -> FJL -> Cape Zhelanya
bool_barnts_1 = N.logical_and(N.logical_and(latitude > 76,latitude <= 81), N.logical_and(longitude>17, longitude <65))
#E limit of Norwegian Sea -> Novaya Zemlya
bool_barnts_2 = N.logical_and(N.logical_and(latitude > 75,latitude < 76), N.logical_and(longitude>17, longitude <62))
bool_barnts_3 = N.logical_and(N.logical_and(latitude > 74,latitude < 75), N.logical_and(longitude>18, longitude <59))
bool_barnts_4 = N.logical_and(N.logical_and(latitude > 73,latitude < 74), N.logical_and(longitude>19, longitude <58))
bool_barnts_5 = N.logical_and(N.logical_and(latitude > 72,latitude < 73), N.logical_and(longitude>21, longitude <56))
bool_barnts_6 = N.logical_and(N.logical_and(latitude > 71,latitude < 72), N.logical_and(longitude>23, longitude <56))
bool_barnts_7 = N.logical_and(N.logical_and(latitude > 70,latitude < 71), N.logical_and(longitude>25, longitude <57))
#I reached North Cape and Kara Gate Strait
bool_barnts_8 = N.logical_and(N.logical_and(latitude > 66,latitude < 70), N.logical_and(longitude>25, longitude <60))
#I fill the White Sea
bool_barnts_9 = N.logical_and(N.logical_and(latitude > 63,latitude < 66), N.logical_and(longitude>30, longitude <45))
bool_barnts = bool_barnts_1
for i in range(2,10):
 exec('bool_barnts=N.logical_or(bool_barnts,bool_barnts_'+ str(i) +')')
#
barentsx = N.where(bool_barnts, mask_v, 0)
#barentsx[274:276,278]=0.
#barentsx[274,279]=0.
dom_dict['BARENTSX'] = barentsx
dom_arct['BARENTSX'] = barentsx
lname_dict['BARENTSX'] = 'Barents Sea'
#
#
#Kara Sea
#Northern part: FJL - Svernya Zemlya - Cape Chelyuskin - Cape Zhelanya
bool_kara_1 = N.logical_and(N.logical_and(latitude > 79,latitude <= 81), N.logical_and(longitude>65, longitude <96))
bool_kara_2 = N.logical_and(N.logical_and(latitude > 76,latitude <= 79), N.logical_and(longitude>65, longitude <105))
#I fill southwestern part of the sea
bool_kara_3 = N.logical_and(N.logical_and(latitude > 75,latitude < 76), N.logical_and(longitude>62, longitude <100))
bool_kara_4 = N.logical_and(N.logical_and(latitude > 74,latitude < 75), N.logical_and(longitude>59, longitude <100))
bool_kara_5 = N.logical_and(N.logical_and(latitude > 73,latitude < 74), N.logical_and(longitude>58, longitude <100))
bool_kara_6 = N.logical_and(N.logical_and(latitude > 71,latitude < 73), N.logical_and(longitude>56, longitude <100))
bool_kara_7 = N.logical_and(N.logical_and(latitude > 70,latitude < 71), N.logical_and(longitude>57, longitude <100))
#I reached Kara Gate Strait and Yamal coast
bool_kara_8 = N.logical_and(N.logical_and(latitude > 66,latitude < 70), N.logical_and(longitude>60, longitude <90))
bool_kara = bool_kara_1
for i in range(2,9):
 exec('bool_kara=N.logical_or(bool_kara,bool_kara_'+ str(i) +')')

karaxxxx = N.where(bool_kara, mask_v, 0)
dom_dict['KARAXXXX'] = karaxxxx
dom_arct['KARAXXXX'] = karaxxxx
lname_dict['KARAXXXX'] = 'Kara Sea'
#
#
#Laptev Sea
#
bool_lapt_1 =  N.logical_and(N.logical_and(latitude > 80,latitude < 81), N.logical_and(longitude>96, longitude <102))
bool_lapt_2 =  N.logical_and(N.logical_and(latitude > 79,latitude < 80), N.logical_and(longitude>100, longitude <111))
bool_lapt_3 =  N.logical_and(N.logical_and(latitude > 78,latitude < 79), N.logical_and(longitude>105, longitude <120))
bool_lapt_4 =  N.logical_and(N.logical_and(latitude > 77,latitude < 78), N.logical_and(longitude>105, longitude <129))
bool_lapt_5 =  N.logical_and(N.logical_and(latitude > 76,latitude < 77), N.logical_and(longitude>100, longitude <138))
#I reached Novaya Zemlya Archipelago: now cross Laptev Strait
bool_lapt_6 =  N.logical_and(N.logical_and(latitude > 70,latitude < 76), N.logical_and(longitude>105, longitude <140))
bool_lapt = bool_lapt_1
for i in range(2,7):
 exec('bool_lapt=N.logical_or(bool_lapt,bool_lapt_'+ str(i) +')')

laptevxx = N.where(bool_lapt, mask_v, 0)
dom_dict['LAPTEVXX'] = laptevxx
dom_arct['LAPTEVXX'] = laptevxx
lname_dict['LAPTEVXX'] = 'Laptev Sea'
#
#
#East Siberian Sea
#
bool_easib_1 = N.logical_and(N.logical_and(latitude > 74,latitude < 75), N.logical_and(longitude>140, longitude <146))
bool_easib_2 = N.logical_and(N.logical_and(latitude > 73,latitude < 74), N.logical_and(longitude>140, longitude <154))
bool_easib_3 = N.logical_and(N.logical_and(latitude > 72,latitude < 73), N.logical_and(longitude>140, longitude <162))
bool_easib_4 = N.logical_and(N.logical_and(latitude > 71,latitude < 72), N.logical_and(longitude>140, longitude <170))
bool_easib_5 = N.logical_and(N.logical_and(latitude > 70,latitude < 71), N.logical_and(longitude>140, longitude <179))
#I reached Wrangel Island (and it is so beautiful)
bool_easib_6 = N.logical_and(N.logical_and(latitude > 69,latitude < 70), N.logical_and(longitude>140, longitude <178))
bool_easib_7 = N.logical_and(N.logical_and(latitude > 68,latitude < 69), N.logical_and(longitude>140, longitude <178))
bool_easib = bool_easib_1
for i in range(2,8):
 exec('bool_easib=N.logical_or(bool_easib,bool_easib_'+ str(i) +')')

eastsibe = N.where(bool_easib,mask_v,0)
dom_dict['EASTSIBE'] = eastsibe
dom_arct['EASTSIBE'] = eastsibe
lname_dict['EASTSIBE'] = 'East Siberian Sea'
#
#
#Chukchi Sea
#
bool_chuk_1 = N.logical_and(N.logical_and(latitude > 66,latitude < 71), longitude <-156)
bool_chuk_2 = N.logical_and(N.logical_and(latitude > 66,latitude < 71), longitude>179)
bool_chuk_3 = N.logical_and(N.logical_and(latitude > 69,latitude < 70), longitude>178)
bool_chuk = N.logical_or(bool_chuk_1,bool_chuk_2)
bool_chuk = N.logical_or(bool_chuk,bool_chuk_3)
chukchis = N.where(bool_chuk,mask_v,0)
dom_dict['CHUKCHIS'] = chukchis
dom_arct['CHUKCHIS'] = chukchis
lname_dict['CHUKCHIS'] = 'Chukchi Sea'
#
#
#Bering Sea
#
bool_bering_1 = N.logical_and(N.logical_and(latitude > 58,latitude < 66), longitude <-154)
bool_bering_2 = N.logical_and(N.logical_and(latitude > 60,latitude < 66), longitude>164)
bool_bering_3 = N.logical_and(N.logical_and(latitude > 57,latitude < 60), longitude>163)
bool_bering_4 = N.logical_and(N.logical_and(latitude > 58,latitude < 60), longitude<-155)
bool_bering_5 = N.logical_and(N.logical_and(latitude > 57,latitude < 58), N.logical_or(longitude<-157, longitude>163))
bool_bering_6 = N.logical_and(N.logical_and(latitude > 56,latitude < 57), N.logical_or(longitude<-160, longitude>167))
bool_bering_7 = N.logical_and(N.logical_and(latitude > 55,latitude < 56), N.logical_or(longitude<-165, longitude>171))
bool_bering_8 = N.logical_and(N.logical_and(latitude > 54,latitude < 55), N.logical_or(longitude<-170, longitude>174))
bool_bering_9 = N.logical_and(N.logical_and(latitude > 53,latitude < 54), N.logical_or(longitude<-174, longitude>177))
bool_bering_10 = N.logical_and(N.logical_and(latitude > 52,latitude < 53), longitude<-178)

bool_bering = bool_bering_1
for i in range(2,11):
 exec('bool_bering=N.logical_or(bool_bering,bool_bering_'+ str(i) +')')

beringx = N.where(bool_bering,mask_v,0)
dom_dict['BERINGXX'] = beringx
dom_arct['BERINGXX'] = beringx
lname_dict['BERINGXX'] = 'Bering Sea'
#
#
#Okhotsk Sea
#First step: Kuriles archipelago and Sakhaline Island
bool_okhot_1 = N.logical_and(N.logical_and(latitude > 43,latitude < 44), N.logical_and(longitude>142, longitude <145))
bool_okhot_2 = N.logical_and(N.logical_and(latitude > 44,latitude < 45), N.logical_and(longitude>142, longitude <146.5))
bool_okhot_3 = N.logical_and(N.logical_and(latitude > 45,latitude < 46), N.logical_and(longitude>142, longitude <148))
bool_okhot_4 = N.logical_and(N.logical_and(latitude > 46,latitude < 47), N.logical_and(longitude>142, longitude <149.5))
bool_okhot_5 = N.logical_and(N.logical_and(latitude > 47,latitude < 48), N.logical_and(longitude>143, longitude <151))
bool_okhot_6 = N.logical_and(N.logical_and(latitude > 48,latitude < 49), N.logical_and(longitude>143, longitude <152.5))
bool_okhot_7 = N.logical_and(N.logical_and(latitude > 49,latitude < 50), N.logical_and(longitude>143, longitude <154))
bool_okhot_8 = N.logical_and(N.logical_and(latitude > 50,latitude < 51), N.logical_and(longitude>143, longitude <155.5))
bool_okhot_9 = N.logical_and(N.logical_and(latitude > 51,latitude < 52), N.logical_and(longitude>143, longitude <157))
#I am at the southernmost point of Kamtchatka
bool_okhot_10 = N.logical_and(N.logical_and(latitude > 52,latitude < 63), N.logical_and(longitude>135, longitude <157))
bool_okhot_11 = N.logical_and(N.logical_and(latitude > 58,latitude < 63), N.logical_and(longitude>157, longitude <163))
bool_okhot_12 = N.logical_and(N.logical_and(latitude > 60,latitude < 63), N.logical_and(longitude>162, longitude <164))
bool_okhot = bool_okhot_1
for i in range(2,13):
 exec('bool_okhot=N.logical_or(bool_okhot,bool_okhot_'+ str(i) +')')

okhotskx = N.where(bool_okhot, mask_v, 0)
dom_dict['OKHOTSKX'] = okhotskx
dom_arct['OKHOTSKX'] = okhotskx
lname_dict['OKHOTSKX'] = 'Okhotsk Sea'
#
#Beaufort Sea !!!!Peut etre a revoir (NW PASSAGE)!!!!
#
bool_beauf_1 = N.logical_and(N.logical_and(latitude > 75,latitude < 76), N.logical_and(longitude>-130, longitude <-124))
bool_beauf_2 = N.logical_and(N.logical_and(latitude > 74,latitude < 75), N.logical_and(longitude>-136, longitude <-124))
bool_beauf_3 = N.logical_and(N.logical_and(latitude > 73,latitude < 74), N.logical_and(longitude>-143, longitude <-125))
bool_beauf_4 = N.logical_and(N.logical_and(latitude > 72,latitude < 73), N.logical_and(longitude>-149, longitude <-125))
bool_beauf_5 = N.logical_and(N.logical_and(latitude > 71,latitude < 72), N.logical_and(longitude>-156, longitude <-126))
bool_beauf_6 = N.logical_and(N.logical_and(latitude > 70,latitude < 71), N.logical_and(longitude>-156, longitude <-126))
bool_beauf_7 = N.logical_and(N.logical_and(latitude > 69,latitude < 70), N.logical_and(longitude>-156, longitude <-127))
bool_beauf_8 = N.logical_and(N.logical_and(latitude > 73,latitude < 77), N.logical_and(longitude>-124, longitude <-120))
bool_beauf_9 = N.logical_and(N.logical_and(latitude > 73,latitude < 75), N.logical_and(longitude>-125, longitude <-124))
bool_beauf_10 = N.logical_and(N.logical_and(latitude > 69,latitude < 73), N.logical_and(longitude>-127, longitude <-124))
bool_beauf = bool_beauf_1
for i in range(2,11):
 exec('bool_beauf=N.logical_or(bool_beauf,bool_beauf_'+ str(i) +')')

beaufort = N.where(bool_beauf, mask_v, 0)
dom_dict['BEAUFORT'] = beaufort
dom_arct['BEAUFORT'] = beaufort
lname_dict['BEAUFORT'] = 'Beaufort Sea'
#
#
#Baffin Bay (including Kennedy Passage and Davis Strait)
#
bool_baff_1 = N.logical_and(N.logical_and(latitude > 70,latitude < 81), N.logical_and(longitude>-84, longitude <-45))
#Now, it is the official definition of Davis Strait...
bool_baff_2 = N.logical_and(N.logical_and(latitude > 66,latitude < 70), N.logical_and(longitude>-70, longitude <-45))
bool_baff_3 = N.logical_and(N.logical_and(latitude > 62,latitude < 66), N.logical_and(longitude>-66, longitude <-45))
bool_baff_4 = N.logical_and(N.logical_and(latitude > 61,latitude < 62), N.logical_and(longitude>-65, longitude <-45))
bool_baff = bool_baff_1
for i in range(2,5):
 exec('bool_baff=N.logical_or(bool_baff,bool_baff_'+ str(i) +')')

baffinxx = N.where(bool_baff,mask_v,0)
dom_dict['BAFFINXX'] = baffinxx
dom_arct['BAFFINXX'] = baffinxx
lname_dict['BAFFINXX'] = 'Baffin Bay'
#
#
#Hudson Bay (including Hudson Strait and Foxe Basin)
#
bool_huds_1 = N.logical_and(N.logical_and(latitude > 50,latitude < 67), N.logical_and(longitude>-95, longitude <-66))
bool_huds_2 = N.logical_and(N.logical_and(latitude > 67,latitude < 70), N.logical_and(longitude>-85, longitude <-70))
bool_huds_3 = N.logical_and(N.logical_and(latitude > 59,latitude < 62), N.logical_and(longitude>-66, longitude <-65))
bool_huds = bool_huds_1
for i in range(2,4):
 exec('bool_huds=N.logical_or(bool_huds,bool_huds_'+ str(i) +')')

hudsonxx = N.where(bool_huds,mask_v,0)
dom_dict['HUDSONXX'] = hudsonxx
dom_arct['HUDSONXX'] = hudsonxx
lname_dict['HUDSONXX'] = 'Hudson Bay'
#


# Atlantic 30-70N
bool_atl3070NnoH = N.logical_and(bool_atl3070N,N.logical_not(bool_huds))
atl3070NnoH = N.where(bool_atl3070NnoH,mask_v,0)
dom_dict['ATL3070NnoH'] = atl3070NnoH
lname_dict['ATL3070NnoH'] = 'Atlantic Ocean  30-70N latitudinal band without the Hudson bay'

# Atlantic 20-70N
bool_atl2070NnoH = N.logical_and(bool_atl2070N,N.logical_not(bool_huds))
atl2070NnoH = N.where(bool_atl2070NnoH,mask_v,0)
dom_dict['ATL2070NnoH'] = atl2070NnoH
lname_dict['ATL2070NnoH'] = 'Atlantic Ocean  20-70N latitudinal band without the Hudson bay'

#
#Labrador Sea
#
bool_labr_1 = N.logical_and(N.logical_and(latitude > 60,latitude < 61), N.logical_and(longitude>-65, longitude <-45))
bool_labr_2 = N.logical_and(N.logical_and(latitude > 59,latitude < 60), N.logical_and(longitude>-65, longitude <-46))
bool_labr_3 = N.logical_and(N.logical_and(latitude > 58,latitude < 59), N.logical_and(longitude>-64, longitude <-46))
bool_labr_4 = N.logical_and(N.logical_and(latitude > 57,latitude < 58), N.logical_and(longitude>-63, longitude <-47))
bool_labr_5 = N.logical_and(N.logical_and(latitude > 56,latitude < 57), N.logical_and(longitude>-62, longitude <-47))
bool_labr_6 = N.logical_and(N.logical_and(latitude > 55,latitude < 56), N.logical_and(longitude>-61, longitude <-48))
bool_labr_7 = N.logical_and(N.logical_and(latitude > 54,latitude < 55), N.logical_and(longitude>-60, longitude <-48))
bool_labr_8 = N.logical_and(N.logical_and(latitude > 53,latitude < 54), N.logical_and(longitude>-59, longitude <-49))
bool_labr_9 = N.logical_and(N.logical_and(latitude > 52,latitude < 53), N.logical_and(longitude>-58, longitude <-49))
bool_labr_10 = N.logical_and(N.logical_and(latitude > 51,latitude < 52), N.logical_and(longitude>-57, longitude <-50))
bool_labr_11 = N.logical_and(N.logical_and(latitude > 50,latitude < 51), N.logical_and(longitude>-56, longitude <-50))
bool_labr_12 = N.logical_and(N.logical_and(latitude > 49,latitude < 50), N.logical_and(longitude>-56, longitude <-51))
#bool_labr_13 = N.logical_and(N.logical_and(latitude > 48,latitude < 49), N.logical_and(longitude>-54, longitude <-51))
bool_labr = bool_labr_1
for i in range(2,13):
 exec('bool_labr=N.logical_or(bool_labr,bool_labr_'+ str(i) +')')

labrador = N.where(bool_labr,mask_v,0)
dom_dict['LABRADOR'] = labrador
dom_arct['LABRADOR'] = labrador
lname_dict['LABRADOR'] = 'Labrador Sea'
#
#
#Northwest Passage
#Southern part (passage Amundsen + official passage)
bool_nwpa_1 = N.logical_and(N.logical_and(latitude > 73,latitude < 77), N.logical_and(longitude>-120, longitude <-84))
bool_nwpa_2 = N.logical_and(N.logical_and(latitude > 67,latitude < 73), N.logical_and(longitude>-124, longitude <-85))
#Northern part (Sverdrup Basin)
bool_nwpa_3 = N.logical_and(N.logical_and(latitude > 76,latitude < 77), N.logical_and(longitude>-120, longitude <-84))
bool_nwpa_4 = N.logical_and(N.logical_and(latitude > 77,latitude < 78), N.logical_and(longitude>-116, longitude <-84))
bool_nwpa_5 = N.logical_and(N.logical_and(latitude > 78,latitude < 79), N.logical_and(longitude>-108, longitude <-84))
bool_nwpa_6 = N.logical_and(N.logical_and(latitude > 79,latitude < 80), N.logical_and(longitude>-100, longitude <-84))
bool_nwpa_7 = N.logical_and(N.logical_and(latitude > 80,latitude < 81), N.logical_and(longitude>-93, longitude <-84))
bool_nwpa_8 = N.logical_and(N.logical_and(latitude > 81,latitude < 82), N.logical_and(longitude>-85, longitude <-84))
bool_nwpa_9 = N.logical_and(N.logical_and(latitude > 82,latitude < 83), N.logical_and(longitude>-77, longitude <-75))
#I reached Cape Columbia (Ellesmere Island): I can walk toward North Pole!!!
bool_nwpa = bool_nwpa_1
for i in range(2,10):
 exec('bool_nwpa=N.logical_or(bool_nwpa,bool_nwpa_'+ str(i) +')')

nwestpas = N.where(bool_nwpa,mask_v,0)
dom_dict['NWESTPAS'] = nwestpas
dom_arct['NWESTPAS'] = nwestpas
lname_dict['NWESTPAS'] = 'Northwest passage'

#
# Maritime NW Passage !!!
bool_mnwp=N.logical_and(bool_nwpa,latitude<76.)
tmpmnwp=N.where(bool_mnwp,mask_v,0)
#tmpmnwp[280:284,232]=0
#tmpmnwp[287:289,130]=0
dom_dict['MNWESTPA']=tmpmnwp
lname_dict['MNWESTPA'] = 'Maritime Northwest passage'
#
# Route du nord !!!
boolnnwp=N.logical_and(tmpmnwp,latitude>=72.5)
tmpnnwp=N.where(boolnnwp,mask_v,0)
dom_dict['MNWESTPN']=tmpnnwp
lname_dict['MNWESTPN']='Martime Nortwest passage : northern route'
#
# Route du sud !!!
boolsnwp=N.logical_and(tmpmnwp,latitude<72.5)
tmpsnwp=N.where(boolsnwp,mask_v,0)
dom_dict['MNWESTPS']=tmpsnwp
lname_dict['MNWESTPS']='Martime Nortwest passage : southern route'
#
#
#Lincoln Sea
bool_linc_1 = N.logical_and(N.logical_and(latitude > 81,latitude < 84), N.logical_and(longitude>-60, longitude <-32))
bool_linc_2 = N.logical_and(N.logical_and(latitude > 81,latitude < 83), N.logical_and(longitude>-70, longitude <-60))
bool_linc = N.logical_or(bool_linc_1,bool_linc_2)

lincolnx = N.where(bool_linc,mask_v,0)
dom_dict['LINCOLNX'] = lincolnx
dom_arct['LINCOLNX'] = lincolnx
lname_dict['LINCOLNX'] = 'Lincoln Sea'
#
#
#Irminger Sea
#
irmin1=N.zeros([149,182])
irmin1[115:123,121:131]=1
bool_irminger=N.logical_and(irmin1==1,ginseasx==0.)
irminger=N.where(bool_irminger,mask_v,0)
dom_dict['IRMINGER']=irminger
lname_dict['IRMINGER']='Irminger Sea'
#
#Marginal seas
dict_marg = ['GINSEASX','BARENTSX','KARAXXXX','BAFFINXX','LAPTEVXX','HUDSONXX','EASTSIBE','BEAUFORT','NWESTPAS','CHUKCHIS','BERINGXX','OKHOTSKX',\
		'LINCOLNX','IRMINGER']
marg = mask_v
for sea in dict_marg:
 marg = marg + dom_dict[sea]
#
bool_marg=marg[0]>1
dom_dict2d['MIZSEASX'] = N.where(bool_marg,mask_v[0],0)
dom_arct2d['MIZSEASX'] = N.where(bool_marg,mask_v[0],0)
lname_dict['MIZSEASX'] = 'Marginal Ice Zone Seas'
#
# IPSL and CNRM marginal seas
# ---------------------------
# Larbador
bool_labipsl = N.logical_and(N.logical_and(latitude>43,latitude<80),N.logical_and(longitude<-40,longitude>-75))
labipsl = N.where(bool_labipsl,mask_v,0)
dom_dict['LABIPSL']=labipsl
lname_dict['LABIPSL'] = 'Labrador Sea in IPSL-CM'
#
# Okhotsk
bool_okhipsl = N.logical_and(N.logical_and(latitude>43,latitude<70),N.logical_and(longitude>133,longitude<163))
okhipsl = N.where(bool_okhipsl,mask_v,0)
dom_dict['OKHIPSL']=okhipsl
lname_dict['OKHIPSL'] = 'Okhotsk Sea in IPSL-CM'
#
bool_okhcnrm = N.logical_and(N.logical_and(latitude>43,latitude<70),N.logical_and(longitude>133,longitude<165))
okhcnrm = N.where(bool_okhcnrm,mask_v,0)
dom_dict['OKHCNRM']=okhcnrm
lname_dict['OKHCNRM'] = 'Okhotsk Sea in CNRM-CM'
#
# Irminger 
bool_irmipsl=N.logical_and(N.logical_and(latitude>55,latitude<67),N.logical_and(longitude>-40,longitude<-20))
bool_irmipsl=N.logical_and(bool_irmipsl==1,labipsl==0.)
irmipsl=N.where(bool_irmipsl,mask_v,0)
dom_dict['IRMIPSL']=irmipsl
lname_dict['IRMIPSL'] = 'Irminger Sea in IPSL-CM'
#
# GIN
bool_ginipsl=N.logical_and(ginseasx==1,bool_barnts==0)
ginipsl=N.where(bool_ginipsl,mask_v,0)
dom_dict['GINIPSL']=ginipsl
lname_dict['GINIPSL'] = 'GIN Seas in IPSL-CM'

#Central Arctic
bool_centrarc = N.equal(marg,nhemisph)
bool_centrarc = N.logical_and(bool_centrarc, latitude > 70)
bool_centrarc = N.logical_and(bool_centrarc, N.logical_not(bool_linc))
centrarc = N.where(bool_centrarc,mask_v, 0)
dom_dict['CENTRARC'] = centrarc
#dom_dict2d['CENTRARC'] = centrarc[0]
#dom_arct['CENTRARC'] = centrarc[0]
lname_dict['CENTRARC'] = 'Central Arctic'
#
#West Central Arctic
bool_westcarc = N.logical_and(bool_centrarc, N.absolute(longitude)>=90)
wcentarc =  N.where(bool_westcarc,mask_v, 0)
dom_dict['WCENTARC'] = wcentarc
#dom_dict2d['WCENTARC'] = wcentarc[0]
lname_dict['WCENTARC'] = 'West Central Arctic'
#
#East Central Arctic
bool_eastcarc = N.logical_and(bool_centrarc, N.absolute(longitude)<90)
ecentarc =  N.where(bool_eastcarc,mask_v, 0)
dom_dict['ECENTARC'] = ecentarc
#dom_dict2d['ECENTARC'] = ecentarc[0]
lname_dict['ECENTARC'] = 'East Central Arctic'
#
#
#
#Arctic Ocean
#
bool_arctic_1 = N.greater(marg,nhemisph)
bool_arctic = N.logical_and(bool_arctic_1,latitude>0)
arcticoc = N.where(N.logical_or(bool_arctic,bool_centrarc),mask_v,0)
dom_dict2d['ARCTICOC'] = arcticoc[0]
lname_dict['ARCTICOC'] = 'Arctic Ocean'
#
# 
#
#
#Baltic Sea
#Gulfs of Bothnia, Riga, Finland.
bool_balt_1 = N.logical_and(N.logical_and(latitude > 50,latitude < 66), N.logical_and(longitude>15, longitude <30))
#South of Sweden until Copenhaguen
bool_balt_2 = N.logical_and(N.logical_and(latitude > 50,latitude < 56), N.logical_and(longitude>10, longitude <15))
bool_balt = bool_balt_1
bool_balt = N.logical_or(bool_balt, bool_balt_2)
baltseax = N.where(bool_balt,mask_v,0)
dom_dict['BALTICXX'] = baltseax
dom_arct['BALTICXX'] = baltseax
lname_dict['BALTICXX'] = 'Baltic Sea'
#
#
#Caspian Sea (for fun)
bool_casp = N.logical_and(N.logical_and(latitude > 35,latitude < 50), N.logical_and(longitude>45, longitude <60))
caspianx = N.where(bool_casp,mask_v,0)
dom_dict['CASPIANX'] = caspianx
lname_dict['CASPIANX'] = 'Caspian Sea'
#
#
# Gulf of Saint-Lawrence
bool_slaw = N.logical_and(N.logical_and(longitude>-70, longitude<-55),N.logical_and(latitude<52,latitude>48))
bool_slaw = N.logical_or(bool_slaw, N.logical_and(N.logical_and(longitude>-70, longitude<-58),N.logical_and(latitude<=48,latitude>47)))
bool_slaw = N.logical_or(bool_slaw, N.logical_and(N.logical_and(longitude>-70, longitude<-59),N.logical_and(latitude<=47,latitude>46)))
bool_slaw = N.logical_or(bool_slaw, N.logical_and(N.logical_and(longitude>-70, longitude<-60),N.logical_and(latitude<=46,latitude>45)))
bool_slaw = N.logical_and(bool_slaw, N.logical_not(bool_labr))
slawrglf=N.where(bool_slaw,mask_v,0)
dom_dict['SLAWRGLF']=slawrglf
dom_arct['SLAWRGLF']=slawrglf
lname_dict['SLAWRGLF']='Gulf of Saint-lawrence'
#
#Northern Hemisphere oceanic seas
nhemisptot = nhemisph + caspianx + baltseax
bool_nohemi = N.equal(nhemisptot,nhemisph)
nnhemisp=N.where(bool_nohemi,nhemisph,0)
dom_dict['NNHEMISP'] = nnhemisp
lname_dict['NNHEMISP'] = 'Northern Hemisphere oceanic seas'
#
# Pacific (en construction ... )
# ------- 
fbassin = nc.Dataset('/net/argos/data/parvati/agglod/DATA/IPSLCM/subbasins_orca21.nc')
bool_pac_1 = fbassin.variables['pacmsk'][:,:]
fbassin.close()
bool_pac = N.logical_and(bool_pac_1,latitude<65)
pacific = N.where(bool_pac,mask_v,0)
dom_dict['PACIFIC'] = pacific
lname_dict['PACIFIC'] = 'Pacific Ocean'
#
# Pacific tropical
bool_pactrop20 = N.logical_and(bool_trop20,bool_pac)
pactrop20 = N.where(bool_pactrop20,mask_v,0)
dom_dict['PACTROP20'] = pactrop20
lname_dict['PACTROP20'] = 'Pacific Ocean tropical band (20N and S)'

# Pacifique equatorial
bool_pactrop10 = N.logical_and(bool_trop10,bool_pac)
pactrop10 = N.where(bool_pactrop10,mask_v,0)
dom_dict['PACTROP10'] = pactrop10
lname_dict['PACTROP10'] = 'Pacific Ocean equatorial band 10N and S)'
#
# Pacifique Nord
bool_pacnorth0 = N.logical_and(bool_pac,latitude>0)
pacnorth0 = N.where(bool_pacnorth0,mask_v,0)
dom_dict['PACNORTH0'] = pacnorth0
lname_dict['PACNORTH0'] = 'Pacific Ocean north of 0N'

# Pacifique Nord 10
bool_pacnorth10 = N.logical_and(bool_pac,latitude>10)
pacnorth10 = N.where(bool_pacnorth10,mask_v,0)
dom_dict['PACNORTH10'] = pacnorth10
lname_dict['PACNORTH10'] = 'Pacific Ocean north of 10N'

# Pacifique Nord 20
bool_pacnorth20 = N.logical_and(bool_pac,latitude>20)
pacnorth20 = N.where(bool_pacnorth20,mask_v,0)
dom_dict['PACNORTH20'] = pacnorth20
lname_dict['PACNORTH20'] = 'Pacific Ocean north of 20N'

# Pacifique Nord 30
bool_pacnorth30 = N.logical_and(bool_pac,latitude>30)
pacnorth30 = N.where(bool_pacnorth30,mask_v,0)
dom_dict['PACNORTH30'] = pacnorth30
lname_dict['PACNORTH30'] = 'Pacific Ocean north of 30N'

# Pacifique Nord 50
bool_pacnorth50 = N.logical_and(bool_pac,latitude>50)
pacnorth50 = N.where(bool_pacnorth50,mask_v,0)
dom_dict['PACNORTH50'] = pacnorth50
lname_dict['PACNORTH50'] = 'Pacific Ocean north of 50N'

# Pacifique sud
bool_pacsouth0 = N.logical_and(bool_pac,latitude<0)
pacsouth0 = N.where(bool_pacsouth0,mask_v,0)
dom_dict['PACSOUTH0'] = pacsouth0
lname_dict['PACSOUTH0'] = 'Pacific Ocean south of 0S'

# Pacifique sud 10
bool_pacsouth10 = N.logical_and(bool_pac,latitude<-10)
pacsouth10 = N.where(bool_pacsouth10,mask_v,0)
dom_dict['PACSOUTH10'] = pacsouth10
lname_dict['PACSOUTH10'] = 'Pacific Ocean nsouth of 10S'

# Pacifique sud 20
bool_pacsouth20 = N.logical_and(bool_pac,latitude<-20)
pacsouth20 = N.where(bool_pacsouth20,mask_v,0)
dom_dict['PACSOUTH20'] = pacsouth20
lname_dict['PACSOUTH20'] = 'Pacific Ocean south of 20S'

# Pacifique south 30
bool_pacsouth30 = N.logical_and(bool_pac,latitude<-30)
pacsouth30 = N.where(bool_pacsouth30,mask_v,0)
dom_dict['PACSOUTH30'] = pacsouth30
lname_dict['PACSOUTH30'] = 'Pacific Ocean south of 30S'

# Pacifique South 50
bool_pacsouth50 = N.logical_and(bool_pac,latitude<-50)
pacsouth50 = N.where(bool_pacsouth50,mask_v,0)
dom_dict['PACSOUTH50'] = pacsouth50
lname_dict['PACSOUTH50'] = 'Pacific Ocean south of 50S'

# Pacifique bande 0-10
bool_pac0010N = N.logical_and(bool_pac,bool_0010N)
pac0010N = N.where(bool_pac0010N,mask_v,0)
dom_dict['PAC0010N'] = pac0010N
lname_dict['PAC0010N'] = 'Pacific Ocean in 0-10N zonal band)'

# Pacique bande 10-20N
bool_pac1020N = N.logical_and(bool_pac,bool_1020N)
pac1020N = N.where(bool_pac1020N,mask_v,0)
dom_dict['PAC1020N'] = pac1020N
lname_dict['PAC1020N'] = 'Pacific Ocean in 10-20N zonal band)'

# Pacique bande 20-30N
bool_pac2030N = N.logical_and(bool_pac,bool_2030N)
pac2030N = N.where(bool_pac2030N,mask_v,0)
dom_dict['PAC2030N'] = pac2030N
lname_dict['PAC2030N'] = 'Pacific Ocean in 20-30N zonal band)'

# Pacique bande 30-40N
bool_pac3040N = N.logical_and(bool_pac,bool_3040N)
pac3040N = N.where(bool_pac3040N,mask_v,0)
dom_dict['PAC3040N'] = pac3040N
lname_dict['PAC3040N'] = 'Pacific Ocean in 30-40N zonal band)'

# Pacique bande 40-50N
bool_pac4050N = N.logical_and(bool_pac,bool_4050N)
pac4050N = N.where(bool_pac4050N,mask_v,0)
dom_dict['PAC4050N'] = pac4050N
lname_dict['PAC4050N'] = 'Pacific Ocean in 40-50N zonal band)'

# Pacique bande 50-60N
bool_pac5060N = N.logical_and(bool_pac,bool_5060N)
pac5060N = N.where(bool_pac5060N,mask_v,0)
dom_dict['PAC5060N'] = pac5060N
lname_dict['PAC5060N'] = 'Pacific Ocean in 50-60N zonal band)'

# Pacique bande 50-70N
bool_pac5070N = N.logical_and(bool_pac,bool_5070N)
pac5070N = N.where(bool_pac5070N,mask_v,0)
dom_dict['PAC5070N'] = pac5070N
lname_dict['PAC5070N'] = 'Pacific Ocean in 50-70N zonal band)'


# ==========================================================================
# NINO
# ==========================================================================
# El nino3
bool_nino3 = N.logical_and(N.logical_and(latitude > -5,latitude < 5), N.logical_and(longitude > -150, longitude < -90))
nino3 = N.where(bool_nino3,mask_v,0)
dom_dict['NINO3'] = nino3
lname_dict['NINO3'] = 'El Nino boxe 3 (5S-5N; 150W-90W)'

# El nino3bis
bool_nino3bis = N.logical_and(N.logical_and(latitude > -5,latitude < 5), N.logical_and(longitude > -120, longitude < -80))
nino3bis = N.where(bool_nino3bis,mask_v,0)
dom_dict['NINO3bis'] = nino3bis
lname_dict['NINO3bis'] = 'Personal El Nino box (5S-5N; 120W-80W)'


# El nino3.4
bool_nino34 = N.logical_and(N.logical_and(latitude > -5,latitude < 5), N.logical_and(longitude > -170, longitude < -120))
nino34 = N.where(bool_nino34,mask_v,0)
dom_dict['NINO34'] = nino34
lname_dict['NINO34'] = 'El Nino boxe 3.4 (5S-5N; 170W-120W)'

# ==========================================================================
# NIN STRAITS
# ==========================================================================
#Fram Strait (Northernmost Greenland Sea)
bool_fram = N.zeros(mask_v.shape[1:])
bool_fram[136,131:140]=1
fram = N.where(bool_fram,mask_v,0)
dom_dict['FRAMSTRX'] = fram
lname_dict['FRAMSTRX'] = 'Fram Strait'
#
#
#Bering Strait (Southernmost Chukchi Sea: in Chk Sea)
bool_bers= N.logical_and(N.logical_and(latitude > 65,latitude < 66), N.logical_and(longitude > -175 , longitude <-165))
beringst = N.where(bool_bers,mask_v,0)
dom_dict['BRNGSTRX'] = beringst
lname_dict['BRNGSTRX'] = 'Bering Strait'
#bool_chuk_1 = N.logical_and(N.logical_and(latitude > 66,latitude < 71), longitude <-156)
#bool_chuk_2 = N.logical_and(N.logical_and(latitude > 66,latitude < 71), longitude>179)
#
#
#Nares Strait (Northernmost Baffin Bay)
bool_nares = N.logical_and(N.logical_and(latitude > 80,latitude < 81), N.logical_and(longitude > -84 , longitude <-45))
narestr = N.where(bool_nares,mask_v,0)
dom_dict['NARESTRX'] = narestr
lname_dict['NARESTRX'] = 'Nares Strait'
#
#
#Kara Gate Strait 
bool_kaga_1 = N.logical_and(N.logical_and(latitude > 70,latitude < 71), N.logical_and(longitude>57, longitude <59))
bool_kaga_2 = N.logical_and(N.logical_and(latitude > 69,latitude < 70), N.logical_and(longitude>60, longitude <61))
bool_kaga = bool_kaga_1
bool_kaga = N.logical_or(bool_kaga,bool_kaga_2)
karagstr = N.where(bool_kaga,mask_v,0)
dom_dict['KARGSTRX'] = karagstr
lname_dict['KARGSTRX'] = 'Kara Gate Strait'
#
#
#Vilkitsky Strait
bool_vilk_1 = N.logical_and(N.logical_and(latitude > 76,latitude <= 79), N.logical_and(longitude>100, longitude <105))
bool_vilk_2 = N.logical_and(N.logical_and(latitude > 70,latitude < 76), N.logical_and(longitude>99, longitude <100))
bool_vilk = bool_vilk_1
bool_vilk = N.logical_or(bool_vilk,bool_vilk_2)
vilkystr = N.where(bool_vilk,mask_v,0)
dom_dict['VILKSTRX'] = vilkystr
lname_dict['VILKSTRX'] = 'Vikitsky Strait'
#
#
#Simple boxes splitting the Antarctic Ocean...
#
#Weddell Sea
#
bool_weddll = N.logical_and(latitude<-50, N.logical_and(longitude>-65, longitude <-15))
weddellx = N.where(bool_weddll,mask_v,0)
dom_dict['WEDDELLX'] = weddellx
lname_dict['WEDDELLX'] = 'Weddell Sea box'
#
#
#Ross Sea
#
bool_ross_1 = N.logical_and(latitude<-50,longitude <-140)
bool_ross_2 = N.logical_and(latitude<-50, longitude>160)
bool_ross = N.logical_or(bool_ross_1,bool_ross_2)
rossxxxx = N.where(bool_ross,mask_v,0)
dom_dict['ROSSXXXX'] = rossxxxx
lname_dict['ROSSXXXX'] = 'Ross Sea box'
#
#
#Amundsen Sea
#
bool_amund = N.logical_and(latitude<-50, N.logical_and(longitude>-140, longitude <-90))
amundsen = N.where(bool_amund,mask_v,0)
dom_dict['AMUNDSEN'] = amundsen
lname_dict['AMUNDSEN'] = 'Amundsen Sea box'
#
#
#Bellingshausen Sea
#
bool_bellings = N.logical_and(latitude<-50, N.logical_and(longitude>-90, longitude <-65))
bellings = N.where(bool_bellings,mask_v,0)
dom_dict['BELLINGS'] = bellings
lname_dict['BELLINGS'] = 'Bellingshausen Sea box'
#
# Bellings+Amundsen
bellamun=amundsen+bellings
dom_dict['BELLAMUN']=bellamun
lname_dict['BELLAMUN']='Bellings + Amundsen boxes'
#
# Atlantic-Antarctic
#
bool_atlantxx_1 = N.logical_and(latitude<-50, longitude>-15)
bool_atlantxx_2 = N.logical_and(latitude<-50, longitude <22)
bool_atlantxx = N.logical_and(bool_atlantxx_1,bool_atlantxx_2)
atlantxx = N.where(bool_atlantxx,mask_v,0)
dom_dict['ATLANTXX'] = atlantxx
lname_dict['ATLANTXX'] = 'Atlantic-Antarctic'
#
# Indian Ocean
# ------------
#
bool_indian = N.logical_and(N.logical_and(latitude>-40, latitude < 30), N.logical_and(longitude>22, longitude <120))
indian = N.where(bool_indian,mask_v,0)
dom_dict['INDIAN'] = indian
lname_dict['INDIAN'] = 'Indian Ocean'
#
# WTIO
bool_wtio = N.logical_and(N.logical_and(latitude>-10, latitude < 10), N.logical_and(longitude>50, longitude <70))
wtio = N.where(bool_wtio,mask_v,0)
dom_dict['WTIO'] = wtio
lname_dict['WTIO'] = 'West tropical Indian Ocean (Standard)'
#
# SETIO
bool_setio = N.logical_and(N.logical_and(latitude>-10, latitude < 0), N.logical_and(longitude>90, longitude <110))
setio = N.where(bool_setio,mask_v,0)
dom_dict['SETIO'] = setio
lname_dict['SETIO'] = 'SouthEastern tropical Indian Ocean (Standard)'
#
# Bay of Bengal
bool_bbengal = N.logical_and(N.logical_and(latitude>5,latitude < 30), N.logical_and(longitude>79, longitude <100))
bbengal = N.where(bool_bbengal,mask_v,0)
dom_dict['BBENGAL'] = bbengal
lname_dict['BBENGAL'] = 'Bay of Bengal'
#
#
# Indian-Antarctic
#
bool_indiant = N.logical_and(latitude<-50, N.logical_and(longitude>22, longitude <160))
indiantx = N.where(bool_indiant,mask_v,0)
dom_dict['INDIANTX'] = indiantx
lname_dict['INDIANTX'] = 'Indian-Antarctic'
#
# NSIDC WEDDELL
nsiweddell=weddellx + atlantxx
dom_dict['NSIWDDEL']=nsiweddell
lname_dict['NSIWDDEL']='NSIDC Weddell Sea'
#
# NSIDC INDIAN
boolnsindian=N.logical_and(bool_indiant,longitude<90.)
nsindiantx=N.where(boolnsindian,mask_v,0.)
dom_dict['NSINDANT']=nsindiantx
lname_dict['NSINDANT']='NSIDC Indian-Antarctic'
#
# NSIDC PACIFIC
boolnsipacant=N.logical_and(bool_indiant,longitude>=90.)
nsipacantx=N.where(boolnsipacant,mask_v,0.)
dom_dict['NSIPFANT']=nsipacantx
lname_dict['NSIPFANT']='NSIDC Pacific-Antarctic'

#
#Other domains: lat
lat80n = N.where(latitude>80.,mask_v,0.)
dom_dict['LAT80N']=lat80n
lname_dict['LAT80N']='North of 80N'
#
#
# COMBINAISON DE REGION (PLUS PERTINENTE)
#
# Barents + Kara Seas
#
dom_dict['BARKARAS']=dom_dict['BARENTSX']+dom_dict['KARAXXXX']
lname_dict['BARKARAS']='Barents + Kara Seas'
#
# East Sib + Laptev Seas
#
dom_dict['ESIBLAPT']=dom_dict['EASTSIBE']+dom_dict['LAPTEVXX']
lname_dict['ESIBLAPT']='East Sib + Laptev Seas'
#
# Canadian Archipelago
#
dom_dict['CANADIAN']=dom_dict['NWESTPAS']+dom_dict['BAFFINXX']+dom_dict['HUDSONXX']+dom_dict['LABRADOR']
lname_dict['CANADIAN']='Canadian Archipelago'
#
# Beaufort + Chukchi Seas
# 
dom_dict['BEAUCHUK']=dom_dict['BEAUFORT']+dom_dict['CHUKCHIS']
lname_dict['BEAUCHUK']='Beaufort + Chukchi Seas'
#
# East Sib + Laptev + Chukchi Seas
#
dom_dict['ESBLAPCH']=dom_dict['ESIBLAPT']+dom_dict['CHUKCHIS']
lname_dict['ESBLAPCH']='East Sib + Laptev + Chukchi Seas'
#
# GIN + Barents Seas
#
dom_dict['GINSBARS']=dom_dict['GINSEASX']+dom_dict['BARENTSX']
lname_dict['GINSBARS']='GIN + Barents Seas'
#
#
# Mask Serreze
boolarcticxx=dom_dict['CENTRARC']+dom_dict['BARENTSX']+\
		dom_dict['KARAXXXX']+dom_dict['LAPTEVXX']+\
		dom_dict['EASTSIBE']+dom_dict['CHUKCHIS']+\
		dom_dict['BEAUFORT']+dom_dict['LINCOLNX']
boolamundsen=N.logical_and(nwestpas,longitude<-113.)
dom_dict['ARCTICXX']=boolarcticxx+boolamundsen
lname_dict['ARCTICXX']='Serreze Arctic Ocean'
#
#mm=x.defmesh(boolarcticxx,refmesh='polar_N')
#pl=x.opentemplate('polar_nu')
#
#
# M'Clintock Channel
mclintock=N.zeros(nwestpas.shape)
#mclintock.setAxisList(nwestpas.getAxisList())
#mclintock[277:283,206:221]=2
#mclintock[278:289,215:225]=2
#mcclintock=N.where(mclintock==2,mask_v,0.)
#dom_dict['MCLINTOC']=mcclintock
#
# Viscount Melville Sound
vmelville=N.zeros(nwestpas.shape)
#vmelville.setAxisList(nwestpas.getAxisList())
#vmelville[284:,131:141]=2
#vmelvilles=N.where(vmelville==2,mask_v,0.)
#dom_dict['VMELVILS']=vmelvilles
#
# Northern Sea Route
#
nsroute=barentsx + karaxxxx + laptevxx + eastsibe + chukchis
dom_dict['NSEROUTE']=nsroute
lname_dict['NSEROUTE']='NSEROUTE'
#
nsroutee=laptevxx + eastsibe + chukchis
nsroutew=barentsx + karaxxxx
dom_dict['ENSROUTE']=nsroutee
lname_dict['ENSROUTE']='ENSROUTE'
dom_dict['WNSROUTE']=nsroutew
lname_dict['WNSROUTE']='WNSROUTE'
#
# COMBINAISON POUR COMPARER AVEC LE NSIDC
# OKOTSKH OK
# BERING OK
# HUDSON OK
# BAFFIN: BAFFIN+LABRADOR
nsbaffin=baffinxx+labrador
#nsbaffin.setAxisList(baffinxx.getAxisList())
dom_dict['NSBAFFIN']=nsbaffin
lname_dict['NSBAFFIN']='NSIDC Baffin + Labrador'
# GREENLAND: GINSEASX+IRMINGER
nsgrnland = ginseasx+irminger
dom_dict['NSGRNLND']=nsgrnland
lname_dict['NSGRNLND']='NSIDC GIN + Irminger Seas'
# BARKARA: OK
# ARCTOCN: CENTRARC+LINCOLN+CHUKCHI+EASTSIB+LAPTEV+BEAUFORT
nsarcton=centrarc[0,...]+lincolnx+chukchis+eastsibe+laptevxx+beaufort
dom_dict['NSARCTON']=nsarcton
lname_dict['NSARCTON']='NSIDC Arctic Central Ocean'
# STLAWR: OK
# OPENOCEN: NNHEMISP - ARCTICOC - LABRADOR - STLAW + BALTIC
openocen=nnhemisp-arcticoc[0] - labrador-slawrglf+baltseax
dom_dict['OPENOCEN']=openocen
lname_dict['OPENOCEN']='Open Ocean'
# 
# ARCTIC NSIDC
# 
inhnsidc=nsarcton+openocen+nsbaffin+okhotskx+beringx+\
		hudsonxx+nsgrnland+\
		dom_dict['BARENTSX']+dom_dict['KARAXXXX']+\
		slawrglf+nwestpas
dom_dict['INHNSIDC']=inhnsidc
lname_dict['INHNSIDC']='INHNSIDC'
# 
# NOKHOTSK
#
nokhotsk=inhnsidc-okhotskx
dom_dict['NOKHOTSK']=nokhotsk
lname_dict['NOKHOTSK']='No Okhotsk'
#
#
###########################################################################################################################
fout = nc.Dataset('Mask_ORCA2.nc','w')

fout.createDimension('z',mask_v.shape[0])
fout.createDimension('y',mask_v.shape[1])
fout.createDimension('x',mask_v.shape[2])
#
lons = fout.createVariable('nav_lon','f8',('y','x',))
lats = fout.createVariable('nav_lat','f8',('y','x',))
lons[:,:] = N.float32(longitude)
lats[:,:] = N.float32(latitude)
i=1
dom_image = mask_v
#
datefile = datetime.date.today() 
fout.author="A. Germe"
fout.Date = str(datefile)
fout.comment = "New version with x and y swaped to fits the x and y outputs of IPSL-CM"
for dom in dom_dict:
    dom_var = fout.createVariable(dom,'f8',('z','y','x',))
    dom_var[:,:,:] = dom_dict[dom]
    dom_var.long_name = lname_dict[dom]
    dom_var.short_name = dom
for dom in dom_dict2d:
    dom_var = fout.createVariable(dom,'f8',('y','x',))
    dom_var[:,:] = dom_dict2d[dom]
    dom_var.long_name = lname_dict[dom]
    dom_var.short_name = dom
fout.close()
