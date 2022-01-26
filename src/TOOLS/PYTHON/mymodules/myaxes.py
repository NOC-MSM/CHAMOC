# -*-coding:Latin-1-*
# =========================================================================
import numpy as N
import netCDF4 as nc
import datetime
# =========================================================================
# Class axe des temps
# =========================================================================
class timeaxis :
    """ Objet perso qui definie un axe des temps associé à un champ ou serie
    temporelle.
    Il s'agit en fait d'une array numpy contenant des objets de type classtime, à laquelle j'ai associé qques méthodes.

    axt = timeaxis(values,units,, calendar='noleap',id='timeaxis',origin=None)

    Method disponible :
        list()
        month()
        year()
        day()
        dayofwk()
        dayfoyr()
        2num()
    """
    def __init__(self,values,units,calendar='noleap',id='timeaxis',origin=None) :
        self.values=values
        self.units=units
        self.calendar=calendar
        self.origin=origin
        self.id = id
    #
    # -----------------------------------------------------
    def list(self) :
        """ timeax.list()
        Liste les caractéristiques de l'axe des temps timeax
        """
        print("Caracteristics :")
        print("id : ", self.id )
        print("shape : ", self.values.shape )
        print("units : ", self.units )
        print("Calendar : ", self.calendar )
        if self.origin is not None : print("origin : ", self.origin )
    #
    # -----------------------------------------------------
    def month(self) :
        months = N.array(list(elt.month for elt in self.values))
        return months
    #
    # -----------------------------------------------------
    def year(self) : 
        years = N.array(list(elt.year for elt in self.values))
        return years
    #
    # -----------------------------------------------------
    def day(self) : 
        days = N.array(list(elt.day for elt in self.values))
        return days
    #
    # -----------------------------------------------------
    def dayofwk(self) : 
        days = N.array(list(elt.dayofwk for elt in self.values))
        return days
    #
    # -----------------------------------------------------
    def dayofyr(self) : 
        days = N.array(list(elt.dayofyr for elt in self.values))
        return days
    #
    # -----------------------------------------------------
    def num(self) :
        numval = nc.date2num(self.values,self.units,calendar=self.calendar)
        return numval
    #
    # -----------------------------------------------------

# =========================================================================
# Class axis quelconque
# =========================================================================
class axis :
    """ Objet perso qui definie un axe quelconque

    Method disponible :
        list()
    """
    def __init__(self,values,units=None,id=None) :
        self.values=values
        self.units=units
        self.id=id
    #
    # -----------------------------------------------------
    def list(self) :
        """ timeax.list()
        Liste les caractéristiques de l'axe des temps timeax
        """
        print(self.id, " axis caracteristics :" )
        print("shape : ", self.values.shape )
        if self.units is not None : print("units : ", self.units )
        if self.id is not None : print("id : ", self.id )
        print("Range : ", self.values.min(), self.values.max() )
    #
    #



