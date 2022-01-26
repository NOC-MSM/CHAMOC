# -*-coding:Latin-1 -*
# =========================================================================
import os, os.path
import netCDF4 as nc
import MA
# =========================================================================
class ensemble :
    """ Objet perso qui definie une simulation
    Utilisé ppalement pour definir les repertoires de sorties des diags
    Appelé dans le module direxp.py (perso)
    
    Methodes disponibles : list
    """
    # ======================================================================
    def __init__(self, name, datedeb=None,datefin=None, year=None, stream=None, model_name='IPSLCM5A', group=None, parent=None, grid_atm=None, grid_oce=None, ismember=None, Nmember=None, listmember=None, nickname=None ) :
        # ======================================================================
        self.name = name
        self.datedeb=datedeb
        self.datefin=datefin
        self.year = (int(self.datedeb[0:4]),int(self.datefin[0:4]))
        self.stream = stream
        self.group = group
        self.parent = parent
        self.Nmember = Nmember
        self.listmember = listmember
        self.model = model_name
        self.grid = dict( A=grid_atm, O=grid_oce, I=grid_oce)
        self.nickname = nickname

     # ======================================================================
    def list(self) :
        """ Liste les attributs de l'objet experience""" 
    # ======================================================================
        print "Caracteristics :"
        if self.stream is not None :print "Stream = ", self.stream
        if self.group is not None :print "Group = ", self.group
        if self.parent is not None :print "Parent = ", self.parent
        print "Is part of an ensemble = ", self.ismember
        if self.member is not None :print "Member = ", self.member
        if self.ensemblename is not None :print "Ensemble name = ", self.ensemblename     
        if self.datedeb is not None :print "Date de d�but : ", self.datedeb
        if self.datefin is not None :print "Date de fin : ", self.datefin
        if self.year is not None :print "Years = ", self.year 
        if self.nickname is not None :print "Nickname = ", self.nickname
        
        if self.model is not None :print "Model = ", self.model
        if self.grid['A'] is not None :  print "Atmospheric Grid = ", self.grid['A']
        if self.grid['O'] is not None :  print "Ocean Grid = ", self.grid['O']
        if self.grid['I'] is not None :  print "Sea-Ice Grid = ", self.grid['I']

   # ======================================================================
    

