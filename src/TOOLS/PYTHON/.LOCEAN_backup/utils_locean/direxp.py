# -*-coding:Latin-1 -*
# ========================================================================
from expe import *

# ========================================================================
# Dictionnaire des expé
# ========================================================================
dexp = dict()

# AR5
#####
dexp['piControl2'] = expe('piControl2',datedeb='18000101',datefin='27991231',stream='AR5', year=(1800,2799),group='CTL', grid_oce='ORCA2', ismember=False,nickname='PICTL', directory='/net/cratos/usr/cratos/varclim/IPSLCM5A/PROD/piControl2/')
#
dexp['piControl2j'] = expe('piControl2j',datedeb='20560101',datefin='20561231',stream='AR5', year=(2056,2056),group='CTL', grid_oce='ORCA2', ismember=False,nickname='PICTLj', directory='/net/argos/data/parvati/agglod/simulations/AR5/CTL/piControl2j/')

# HIST
for i in range(1,6) :
    expname='v3.historical%i'%i
    dexp[expname]=expe(expname,datedeb='18500101',datefin='20051231',stream='AR5',group='hist', grid_oce='ORCA2',ismember=True,member=str(i),ensemblename='v3',nickname='HIST'+str(i),parent='piControl2',directory='/net/cratos/usr/cratos/varclim/IPSLCM5A/PROD/historical/%s/'%expname)
#
#
# RCPs
for i in range(1,5) :
    expname='v3.rcp45.%i'%i
    dexp[expname]=expe(expname,datedeb='20060101',datefin='23001231',stream='AR5',group='RCP', grid_oce='ORCA2',ismember=True,member=str(i),ensemblename='RCP45',nickname='RCP45.%i'%i,parent='v3.historical%i'%i,directory='/net/cratos/usr/cratos/varclim/IPSLCM5A/PROD/rcp45/%s/'%expname)
#
for i in range(1,1) :
    expname='v3.rcp85.%i'%i
    dexp[expname]=expe(expname,datedeb='20060101',datefin='20951231',stream='AR5',group='RCP', grid_oce='ORCA2',ismember=True,member=str(i),ensemblename='RCP85',nickname='RCP85.%i'%i,parent='v3.historical%i'%i,directory='/net/cratos/usr/cratos/varclim/IPSLCM5A/PROD/rcp85/%s/'%expname)

# EPCT
######
# EPCT101
for i in ['A','B','C','D','E','F','G','H','I','J'] : 
    expname = 'EPCT101%s'%i
    dexp[expname] = expe(expname,datedeb='19010101',datefin='19201231', stream='DEC',group='EPCT',ismember=True, member=i,ensemblename='EPCT101',grid_oce='ORCA2', directory='/net/cratos/usr/cratos/varclim/IPSLCM5A/EPCT/EPCT101/', parent='piControl2')
#
dexp['EPCT101Z'] = expe('EPCT101Z',datedeb='19010101',datefin='19011231', stream='DEC',group='EPCT',ismember=True, member=i,ensemblename='EPCT101',grid_oce='ORCA2', directory='/net/cratos/usr/cratos/varclim/IPSLCM5A/EPCT/EPCT101/', parent='piControl2')
#
# EPCT256
for i in ['A','B','C','D','E','F','G','H','I','J'] : 
    expname = 'EPCT256%s'%i
    dexp[expname] = expe(expname,datedeb='20560101',datefin='20751231', stream='DEC',group='EPCT',ismember=True, member=i,ensemblename='EPCT256',grid_oce='ORCA2', directory='/net/cratos/usr/cratos/varclim/IPSLCM5A/EPCT/EPCT256/', parent='piControl2')
#
# EPCT266
for i in ['A','B','C','D','E','F','G','H','I','J'] : 
    expname = 'EPCT266%s'%i
    dexp[expname] = expe(expname,datedeb='20660101',datefin='20851231', stream='DEC',group='EPCT',ismember=True, member=i,ensemblename='EPCT266',grid_oce='ORCA2', directory='/net/cratos/usr/cratos/varclim/IPSLCM5A/EPCT/EPCT266/', parent='piControl2')
#
# EPCT271
for i in ['A','B','C','D','E','F','G','H','I','J'] : 
    expname = 'EPCT271%s'%i
    dexp[expname] = expe(expname,datedeb='20710101',datefin='20901231', stream='DEC',group='EPCT',ismember=True, member=i,ensemblename='EPCT271',grid_oce='ORCA2', directory='/net/cratos/usr/cratos/varclim/IPSLCM5A/EPCT/EPCT271/', parent='piControl2')
#
# EPCT371
for i in ['A','B','C','D','E','F','G','H','I','J'] : 
    expname = 'EPCT371%s'%i
    dexp[expname] = expe(expname,datedeb='21710101',datefin='21901231', stream='DEC',group='EPCT',ismember=True, member=i,ensemblename='EPCT371',grid_oce='ORCA2', directory='/net/cratos/usr/cratos/varclim/IPSLCM5A/EPCT/EPCT371/', parent='piControl2')
#
# EPCT191
for i in ['A','B','C','D','E','F','G','H','I','J'] : 
    expname = 'EPCT191%s'%i
    dexp[expname] = expe(expname,datedeb='19910101',datefin='20101231', stream='DEC',group='EPCT',ismember=True, member=i,ensemblename='EPCT191',grid_oce='ORCA2', directory='/net/argos/data/parvati/agglod/simulations/DEC/EPCT/EPCT191/%s/'%(expname), parent='piControl2')
#

# EPCTOP
#######
#
#first tests
dexp['piCtrl0o00031'] = expe('piCtrl0o00031',datedeb='20660101',datefin='20751231',stream='DEC',group='EPCTOP',ismember=True,ensemblename='test266',grid_oce='ORCA2',directory='/net/cratos/usr/cratos/varclim/IPSLCM5A/EPCTOP/piCtrl0o00031/', parent='piControl2')
#
dexp['piCtrlNoSi0o01'] = expe('piCtrlNoSi0o01',datedeb='20660101',datefin='20751231',stream='DEC',group='EPCTOP',ismember=True,ensemblename='test266',grid_oce='ORCA2',directory='/net/cratos/usr/cratos/varclim/IPSLCM5A/EPCTOP/piCtrlNoSi0o01/', parent='piControl2')
#
dexp['piCtrlNoSi0o156'] = expe('piCtrlNoSi0o156',datedeb='20660101',datefin='20751231',stream='DEC',group='EPCTOP',ismember=True,ensemblename='test266',grid_oce='ORCA2',directory='/net/cratos/usr/cratos/varclim/IPSLCM5A/EPCTOP/piCtrlNoSi0o156/', parent='piControl2')
#
dexp['piCtrlNoSi1o56'] = expe('piCtrlNoSi1o56',datedeb='20660101',datefin='20751231',stream='DEC',group='EPCTOP',ismember=True,ensemblename='test266',grid_oce='ORCA2',directory='/net/cratos/usr/cratos/varclim/IPSLCM5A/EPCTOP/piCtrlNoSi1o56/', parent='piControl2')
#
dexp['piCtrl0o01'] = expe('piCtrl0o01',datedeb='20660101',datefin='20691231',stream='DEC',group='EPCTOP',ismember=True,ensemblename='test266',grid_oce='ORCA2',directory='/net/cratos/usr/cratos/varclim/IPSLCM5A/EPCTOP/piCtrl0o01/', parent='piControl2')
#
dexp['piOCE2E3s1o56'] = expe('piOCE2E3s1o56',datedeb='20660101',datefin='20751231',stream='DEC',group='EPCTOP',ismember=True,ensemblename='test266',grid_oce='ORCA2',directory='/net/cratos/usr/cratos/varclim/IPSLCM5A/EPCTOP/piOCE2E3s1o56/',parent='piControl2')
#
dexp['piOCENoise0o1'] = expe('piOCENoise0o1',datedeb='20660101',datefin='20751231',stream='DEC',group='EPCTOP',ismember=True,ensemblename='test266',grid_oce='ORCA2',directory='/net/cratos/usr/cratos/varclim/IPSLCM5A/EPCTOP/piOCENoise0o1/',parent='piControl2')
#
dexp['PWNICE0o1'] = expe('PWNICE0o1',datedeb='20560101',datefin='20651231',stream='DEC',group='EPCTOP',ismember=True,ensemblename='test256',grid_oce='ORCA2',directory='/net/cratos/usr/cratos/varclim/IPSLCM5A/EPCTOP/PWNICE0o1/',parent='piControl2')
#
dexp['PWNNoSi0o1'] = expe('PWNNoSi0o1',datedeb='20560101',datefin='20651231',stream='DEC',group='EPCTOP',ismember=True,ensemblename='test256',grid_oce='ORCA2',directory='/net/cratos/usr/cratos/varclim/IPSLCM5A/EPCTOP/PWNNoSi0o1/',parent='piControl2')

# OWN3D
########
#
# OWN256
indice = 1
for i in ['A','B'] : 
    expname = 'OWN256%s'%i
    dexp[expname] = expe(expname,datedeb='20560101',datefin='20651231', stream='DEC',group='OWN3D',ismember=True, member=i,ensemblename='OWN3D256',grid_oce='ORCA2', directory='/net/argos/data/parvati/agglod/simulations/DEC/OWN3D/OWN3D256/%s/'%(expname), parent='piControl2')
    indice = indice +1
#

# OWN3DT
########
#
# OWN3DT256
for i in ['A','B','C','D','E','F','G','H','I','J'] : 
    expname = 'OWN3DT256%s'%i
    dexp[expname] = expe(expname,datedeb='20560101',datefin='20751231', stream='DEC',group='OWN3DT',ismember=True, member=i,ensemblename='OWN3DT256',grid_oce='ORCA2', directory='/net/argos/data/parvati/agglod/simulations/DEC/OWN3DT/OWN3DT256/%s/'%(expname), parent='piControl2')
#
dexp['OWN3DT256Aj'] = expe('OWN3DT256Aj',datedeb='20560101',datefin='20561231', stream='DEC',group='OWN3DT',ismember=True, member=i,ensemblename='OWN3DT256',grid_oce='ORCA2', directory='/net/argos/data/parvati/agglod/simulations/DEC/OWN3DT/OWN3DT256/OWN3DT256Aj/', parent='piControl2')
#
# OWN3DTdeep
for i in ['A','B','C','D','E','F','G','H','I','J'] : 
    expname = 'OWN3DTdeep%s'%i
    dexp[expname] = expe(expname,datedeb='20560101',datefin='20751231', stream='DEC',group='OWN3DT',ismember=True, member=i,ensemblename='OWN3DTdeep',grid_oce='ORCA2', directory='/net/argos/data/parvati/agglod/simulations/DEC/OWN3DT/OWN3DTdeep/%s/'%(expname), parent='piControl2')
#
dexp['OWN3DTdeepAj'] = expe('OWN3DTdeepAj',datedeb='20560101',datefin='20561231', stream='DEC',group='OWN3DT',ismember=True, member=i,ensemblename='OWN3DTdeep',grid_oce='ORCA2', directory='/net/argos/data/parvati/agglod/simulations/DEC/OWN3DT/OWN3DTdeep/OWN3DTdeepAj/', parent='piControl2')
#
#
# OWN3DT010M
for i in ['A','B','C','D','E','F','G','H','I','J'] : 
    expname = 'OWN3DT010M%s'%i
    dexp[expname] = expe(expname,datedeb='20560101',datefin='20751231', stream='DEC',group='OWN3DT',ismember=True, member=i,ensemblename='OWN3DT010M',grid_oce='ORCA2', directory='/net/argos/data/parvati/agglod/simulations/DEC/OWN3DT/OWN3DT010M/%s/'%(expname), parent='piControl2')
#
dexp['OWN3DT010MAj'] = expe('OWN3DT010MAj',datedeb='20560101',datefin='20561231', stream='DEC',group='OWN3DT',ismember=True, member=i,ensemblename='OWN3DT010M',grid_oce='ORCA2', directory='/net/argos/data/parvati/agglod/simulations/DEC/OWN3DT/OWN3DT010M/OWN3DT010MAj/', parent='piControl2')
#
#
# OWN3DT100M
for i in ['A','B','C','D','E','F','G','H','I','J'] : 
    expname = 'OWN3DT100M%s'%i
    dexp[expname] = expe(expname,datedeb='20560101',datefin='20751231', stream='DEC',group='OWN3DT',ismember=True, member=i,ensemblename='OWN3DT100M',grid_oce='ORCA2', directory='/net/argos/data/parvati/agglod/simulations/DEC/OWN3DT/OWN3DT100M/%s/'%(expname), parent='piControl2')
#

# OP3D
########
#
# OP3DAMTP
dexp['OP3DAMTP'] = expe('OP3DAMTP',datedeb='20560101',datefin='20851231', stream='DEC',group='OP3D',ismember=True,member='P',ensemblename='OP3DAMT',grid_oce='ORCA2', directory='/net/argos/data/parvati/agglod/simulations/DEC/OP3D/OP3DAMTP/', parent='piControl2')
#
# OP3DAMTN
dexp['OP3DAMTN'] = expe('OP3DAMTN',datedeb='20560101',datefin='20851231', stream='DEC',group='OP3D',ismember=True,member='N',ensemblename='OP3DAMT',grid_oce='ORCA2', directory='/net/argos/data/parvati/agglod/simulations/DEC/OP3D/OP3DAMTN/', parent='piControl2')

# LOP
###################
#
# LOPAMTP191
for i in ['A','B','C','D','E'] : 
    expname = 'LOPAMTP191%s'%i
    dexp[expname] = expe(expname,datedeb='19910101',datefin='20101231', stream='DEC',group='LOP',ismember=True, member=i,ensemblename='LOPAMTP191',grid_oce='ORCA2', directory='/net/argos/data/parvati/agglod/simulations/DEC/LOP/LOPAMTP191/%s/'%(expname), parent='piControl2')
#
# LOPAMTP191X05
for i in ['A','B','C','D','E'] : 
    expname = 'LOPAMTP191X05%s'%i
    dexp[expname] = expe(expname,datedeb='19910101',datefin='20101231', stream='DEC',group='LOP',ismember=True, member=i,ensemblename='LOPAMTP191X05',grid_oce='ORCA2', directory='/net/argos/data/parvati/agglod/simulations/DEC/LOP/LOPAMTP191X05/%s/'%(expname), parent='piControl2')
#
# LOPAMTP191X10
for i in ['A','B','C','D','E'] : 
    expname = 'LOPAMTP191X10%s'%i
    dexp[expname] = expe(expname,datedeb='19910101',datefin='20101231', stream='DEC',group='LOP',ismember=True, member=i,ensemblename='LOPAMTP191X10',grid_oce='ORCA2', directory='/net/argos/data/parvati/agglod/simulations/DEC/LOP/LOPAMTP191X10/%s/'%(expname), parent='piControl2')
#
# LOPAMTN191X10
for i in ['A','B','C','D','E'] : 
    expname = 'LOPAMTN191X10%s'%i
    dexp[expname] = expe(expname,datedeb='19910101',datefin='20101231', stream='DEC',group='LOP',ismember=True, member=i,ensemblename='LOPAMTN191X10',grid_oce='ORCA2', directory='/net/argos/data/parvati/agglod/simulations/DEC/LOP/LOPAMTN191X10/%s/'%(expname), parent='piControl2')
#
# LOPAMTP191X20
for i in ['A','B','C','D','E'] : 
    expname = 'LOPAMTP191X20%s'%i
    dexp[expname] = expe(expname,datedeb='19910101',datefin='20101231', stream='DEC',group='LOP',ismember=True, member=i,ensemblename='LOPAMTP191X20',grid_oce='ORCA2', directory='/net/argos/data/parvati/agglod/simulations/DEC/LOP/LOPAMTP191X20/%s/'%(expname), parent='piControl2')


# NUD
#######
#
dexp['v3h4BT00'] = expe('v3h4BT00',datedeb='19490101',datefin='19681231',stream='NUD',group='ERSST',ismember=False,grid_oce='ORCA2',directory='/net/cratos/usr/cratos/varclim/IPSLCM5A/DECENNAL/PROD/historical/v3h4BT00/',parent='v3.historical4')
#
dexp['v3h4CT00NoSi'] = expe('v3h4CT00NoSi',datedeb='19490101',datefin='20121231',stream='NUD',group='ERSST',ismember=False,grid_oce='ORCA2',directory='/net/cratos/usr/cratos/varclim/IPSLCM5A/DECENNAL/PROD/historical/v3h4CT00NoSi/',parent='v3.historical4')

# MIPIPSL
#########
dexp['piControlMR3'] = expe('piControlMR3',datedeb='18000101',datefin='22991231',stream='MIP', year=(1800,2299),group='CTL', grid_oce='ORCA2', ismember=False,nickname='PICTLMR3', directory='/net/cratos/usr/cratos/varclim/IPSLCM5A/MR/PROD/piControlMR3/',model_name='IPSLCM5A-MR')
#
dexp['v5.PiCtrlNP1'] = expe('v5.PiCtrlNP1',datedeb='18300101',datefin='21291231',stream='MIP', year=(1830,2129),group='CTL', grid_oce='ORCA2', ismember=False,nickname='v5.PICTLNP1', directory='/net/cratos/usr/cratos/varclim/IPSLCM5B/piControl/v5.PiCtrlNP1/',model_name='IPSLCM5B')

# ==========================================================================
#                           CNRM-CM5.1
# ==========================================================================
dexp['PICTL-CNRM'] = expe('piControl',datedeb='18500101',datefin='26991231',stream='AR5', year=(1850,2699),group='CTL',grid_oce='ORCA1',ismember=True,member='r1i1p1',nickname='PICTL',model_name='CNRM-CM5',directory='/net/argos/data/parvati/agglod/DATA/CNRM-CM/simulations/CMIP5/CTL/piControl/',format='cmor')
