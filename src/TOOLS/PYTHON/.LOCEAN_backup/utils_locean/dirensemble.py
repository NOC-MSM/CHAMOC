# -*-coding:Latin-1 -*
# ========================================================================
from ensembleclass import *

# ========================================================================
# Dictionnaire des expé
# ========================================================================
dens = dict()
#
# EPCT
#########
dens['EPCT101'] = ensemble('EPCT101',datedeb='19010101',datefin='19201231',stream='DEC',group='EPCT',Nmember=10,grid_oce='ORCA2', parent='piControl2',listmember=['EPCT101A','EPCT101B','EPCT101C','EPCT101D','EPCT101E','EPCT101F','EPCT101G','EPCT101H','EPCT101I','EPCT101J'])
#
dens['EPCT256'] = ensemble('EPCT256',datedeb='20560101',datefin='20751231',stream='DEC',group='EPCT',Nmember=10,grid_oce='ORCA2', parent='piControl2',listmember=['EPCT256A','EPCT256B','EPCT256C','EPCT256D','EPCT256E','EPCT256F','EPCT256G','EPCT256H','EPCT256I','EPCT256J'])
#
dens['EPCT266'] = ensemble('EPCT266',datedeb='20660101',datefin='20851231',stream='DEC',group='EPCT',Nmember=10,grid_oce='ORCA2', parent='piControl2',listmember=['EPCT266A','EPCT266B','EPCT266C','EPCT266D','EPCT266E','EPCT266F','EPCT266G','EPCT266H','EPCT266I','EPCT266J'])
#
dens['EPCT271'] = ensemble('EPCT271',datedeb='20710101',datefin='20901231',stream='DEC',group='EPCT',Nmember=10,grid_oce='ORCA2', parent='piControl2',listmember=['EPCT271A','EPCT271B','EPCT271C','EPCT271D','EPCT271E','EPCT271F','EPCT271G','EPCT271H','EPCT271I','EPCT271J'])
#
dens['EPCT371'] = ensemble('EPCT371',datedeb='21710101',datefin='21901231',stream='DEC',group='EPCT',Nmember=10,grid_oce='ORCA2', parent='piControl2',listmember=['EPCT371A','EPCT371B','EPCT371C','EPCT371D','EPCT371E','EPCT371F','EPCT371G','EPCT371H','EPCT371I','EPCT371J'])
#
#
#
# OWN3DT
########
dens['OWN3DT256'] = ensemble('OWN3DT256',datedeb='20560101',datefin='20751231',stream='DEC',group='OWN3DT',Nmember=10,grid_oce='ORCA2', parent='piControl2',listmember=['OWN3DT256A','OWN3DT256B','OWN3DT256C','OWN3DT256D','OWN3DT256E','OWN3DT256F','OWN3DT256G','OWN3DT256H','OWN3DT256I','OWN3DT256J'])
#
dens['OWN3DTdeep'] = ensemble('OWN3DTdeep',datedeb='20560101',datefin='20751231',stream='DEC',group='OWN3DT',Nmember=10,grid_oce='ORCA2', parent='piControl2',listmember=['OWN3DTdeepA','OWN3DTdeepB','OWN3DTdeepC','OWN3DTdeepD','OWN3DTdeepE','OWN3DTdeepF','OWN3DTdeepG','OWN3DTdeepH','OWN3DTdeepI','OWN3DTdeepJ'])
#
dens['OWN3DT010M'] = ensemble('OWN3DT010M',datedeb='20560101',datefin='20751231',stream='DEC',group='OWN3DT',Nmember=10,grid_oce='ORCA2', parent='piControl2',listmember=['OWN3DT010MA','OWN3DT010MB','OWN3DT010MC','OWN3DT010MD','OWN3DT010ME','OWN3DT010MF','OWN3DT010MG','OWN3DT010MH','OWN3DT010MI','OWN3DT010MJ'])
#
dens['OWN3DT100M'] = ensemble('OWN3DT100M',datedeb='20560101',datefin='20751231',stream='DEC',group='OWN3DT',Nmember=10,grid_oce='ORCA2', parent='piControl2',listmember=['OWN3DT100MA','OWN3DT100MB','OWN3DT100MC','OWN3DT100MD','OWN3DT100ME','OWN3DT100MF','OWN3DT100MG','OWN3DT100MH','OWN3DT100MI','OWN3DT100MJ'])
#


# ===========================================================================
def union(newensemblename,ensemblelist) : 
    """
    newensemble = union(newensemblename,ensemblelist)
    créé un gros ensemble en fusionnant plusieurs ensembles
    """
    # -----------------------------------------------------------------
    if len(ensemblelist)<1 :
        print('Error : no ensemble in ensemblelist')
    #
    ensref = dens[ensemblelist[0]]
    newlistmember = []
    for ensid in ensemblelist :
        newlistmember.extend(dens[ensid].listmember)
    #
    newensemble= ensemble(newensemblename,datedeb=ensref.datedeb,datefin=ensref.datefin,year=ensref.year,listmember=newlistmember)
    #
    return newensemble


# ===========================================================================
# BIG ENSEMBLES
# ===========================================================================
dens['OWN3DT']=union('OWN3DT',['OWN3DT256','OWN3DTdeep','OWN3DT010M']) 
dens['OWN3DTlarge']=union('OWN3DTlarge',['OWN3DT256','OWN3DTdeep','OWN3DT010M','OWN3DT100M']) 
dens['WN']=union('WN',['OWN3DT','EPCT256'])



