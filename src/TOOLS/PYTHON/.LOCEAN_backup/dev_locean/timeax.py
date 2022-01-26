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
    Il s'agit en fait d'une array numpy contenant des objets de type classtime, à laquelle j'ai associé qques méthode

    Method disponible :
        list()
        month()
        year()
        day()
        dayofwk()
        dayfoyr()
        2num()
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
        print "shape : ", self.values.shape
        print "units : ", self.units
        print "Calendar : ", self.calendar
        if self.origin is not None : print "origin : ", self.origin
    #
    # -----------------------------------------------------
    def month(self) :
        months = N.array(list(elt.month for elt in self.values))
        return months
    #
    # -----------------------------------------------------
    def year(self) : 
        years = N.array(list(elt.year for elt in self.values))
        return year
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
        numval = nc.date2num(self.values)
        return numval
    #
    # -----------------------------------------------------
