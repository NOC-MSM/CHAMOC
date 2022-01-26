# -*-coding:Latin-1 -*
# =========================================================================
import os, os.path, sys
import netCDF4 as nc
import MA
# =========================================================================
varlistO={} # dictionnaire contenant les variables selon type de fichier
varlistO['diaptr']=['zomsfglo','zomsfatl','zomsfpac','zomsfind','zomsfipc','sohtatl','sohtpac','sohtind','sohtipc']
varlistO['grid_T']=['thkcello','sosstsst','sosaline','somxl010']
varlistO['scalar']=['masso','volo','sozga','thetaoga','soga']
# -----------------------------------------------------------------
varlistI={}
varlistI['icemod']=['bmelt','evap','grLateral','ialb','iicetemp','iicethic','iicevelu','iicevelv','soicecov','strairx','strairy','tmelt','tsice']
# =========================================================================
class expe :
    """ Objet perso qui definie une simulation
    UtilisÃ© ppalement pour definir les repertoires de sorties des diags
    AppelÃ© dans le module direxp.py (perso)
    
    Methodes disponibles : list
    """
    # ======================================================================
    def __init__(self, name, datedeb=None,datefin=None, year=None, stream=None, model_name='IPSLCM5A', group=None, parent=None, grid_atm=None, grid_oce=None, ismember=None, member=None, ensemblename=None, directory=None, nickname=None ) :
        # ======================================================================
        self.name = name
        self.datedeb=datedeb
        self.datefin=datefin
        self.year = (int(self.datedeb[0:4]),int(self.datefin[0:4]))
        self.stream = stream
        self.group = group
        self.parent = parent
        self.ismember = ismember
        self.member = member
        self.ensemblename = ensemblename
        self.model = model_name
        self.grid = dict( A=grid_atm, O=grid_oce, I=grid_oce)
        self.directory = directory
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
        if self.datedeb is not None :print "Date de début : ", self.datedeb
        if self.datefin is not None :print "Date de fin : ", self.datefin
        if self.year is not None :print "Years = ", self.year 
        if self.nickname is not None :print "Nickname = ", self.nickname
        
        if self.model is not None :print "Model = ", self.model
        if self.grid['A'] is not None :  print "Atmospheric Grid = ", self.grid['A']
        if self.grid['O'] is not None :  print "Ocean Grid = ", self.grid['O']
        if self.grid['I'] is not None :  print "Sea-Ice Grid = ", self.grid['I']

   # ======================================================================
    def loc(self,realm='I') : 
        """
        dirin = exp.loc(realm='I')
        Localise le répertoire contenant les variables du realm
        """
        # -----------------------------------------------------------------
        if self.directory is None : 
            self.directory='/net/cratos/usr/cratos/varclim/IPSLCM5A/%s/%s/%s/'%(self.stream,self.group,self.ensemblename)
        #
        if realm is 'I' : reprealm='ICE/'
        elif realm is 'A' : reprealm='ATM/'
        elif realm is 'O' : reprealm='OCE/'
        dirin=self.directory+reprealm+'Analyse/TS_MO/'
     #
        return dirin
   # ======================================================================
    def locfile(self,varname,realm='I',freq='MO') : 
        """
        dirin = exp.locfile('soicecov',realm='I')
        Localise le fichier contenant les variables du realm
        """
        # ----------------------------------------------------------------
        if self.directory is None : 
            self.directory='/net/cratos/usr/cratos/varclim/IPSLCM5A/%s/%s/%s/'%(self.stream,self.group,self.ensemblename)
        #
        if realm is 'I' : reprealm='ICE/'
        elif realm is 'A' : reprealm='ATM/'
        elif realm is 'O' : reprealm='OCE/'
        #
        cas1=self.directory+reprealm+'Analyse/TS_'+freq+'/'+self.fname(varname)
        if realm is 'I' :            
            cas2=self.directory+reprealm+'Output/'+freq+'/'+self.name+'_'+self.datedeb+'_'+self.datefin+'_1M_icemod.nc'
        elif realm is 'O' :
            if varname in varlistO['diaptr'] :
                 cas2=self.directory+reprealm+'Output/'+freq+'/'+self.name+'_'+self.datedeb+'_'+self.datefin+'_1M_diaptr.nc'
            elif varname in varlistO['grid_T'] :
                cas2=self.directory+reprealm+'Output/'+freq+'/'+self.name+'_'+self.datedeb+'_'+self.datefin+'_1M_grid_T.nc'
            elif varname in varlistO['scalar'] :
                cas2=self.directory+reprealm+'Output/'+freq+'/'+self.name+'_'+self.datedeb+'_'+self.datefin+'_1M_scalar.nc'
            else :
                raise Exception('couldn\'t find the varname %s in realm %s'%(varname,realm))
            #
        if os.path.exists(cas1) : 
            fileloc=cas1
        elif os.path.exists(cas2) :
            fileloc=cas2
        else :
            sys.exit("Couldn\'t find any file for exp: %s, varname: %s, realm: %s"%(self.name,varname,realm))
     #
        return fileloc
# ======================================================================
    def fname(self,varname) :
        """
        filename = exp.filen(varname)
        Donne le nom du fichier contenant la serie temporelle de la variable
        varname pour l'expé exp.
        """
       # ---------------------------------------------------------------
        filename="%s_%s_%s_1M_%s.nc"%(self.name,self.datedeb,self.datefin,varname)
        return filename
    

