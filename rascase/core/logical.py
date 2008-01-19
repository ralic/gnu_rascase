# -*- coding: utf-8 -*-
"""
Este modulo contiene las clases relacionadas con la implementación de las funcionalidades a nivel de modelo para la gestión de 'modelos lógicos'

"""
##
## logical.py
## Login : <freyes@yoda>
## Started on  Sat Jan 19 17:02:59 2008 Felipe Reyes
## $Id$
## 
## Copyright (C) 2008 Felipe Reyes
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
## 
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## 
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##

from rascase.core.base import *

class LogicalModel(base.ModelBase):
    def __init__(self):
        self._entities_list = None
        self._relationships_list = None
        self._inheritance_list = None

    def generate_physical_model(self, path=None):
        return False

    def add_entity(self, entity):
        return False

    def get_entity(self, codename):
        return None
    
    def del_entity(self, codename):
        return False

    def get_all_entites(self):
        return self._entities_list

    
class Entity(LogicalBase, RectBase):
    def __init__(self, x, y):
        self._attributes_list = None

    def add_attribute(self, attribute):
        return False

    def del_attribute(self, attribute):
        return False


class Attribute(LogicalBase):
    def __init__(self):
        self._primary_key = False
        self._data_type = None
        self._default_value = None
        self._mandatory = False

    def set_primary_key(self, value):
        pass

    def is_primary_key(self):
        return False

    def set_default_value(self, value):
        pass

    def get_default_value(self):
        pass

    def set_data_type(self, value):
        pass

    def get_data_type(self):
        pass

    def set_mandatory(self, value):
        pass

    def is_mandatory(self):
        pass


class Relationship(LogicalBase):

    CARDINALITY_1_1 = 0
    CARDINALITY_1_N = 1
    CARDINALITY_N_1 = 2
    CARDINALITY_N_N = 3
    
    def __init__(self, entity1, entity2):
        self._cardinality = None
        self._entity1 = entity1
        self._entity2 = entity2

    def set_cardinality(self, value):
        pass

    def get_cardinality(self):
        pass

    def set_entity1(self, entity):
        pass

    def get_entity1(self):
        pass

    def set_entity2(self, entity):
        pass

    def get_entity2(self):
        pass

class Inheritance(LogicalBase):
    def __init__(self, father, son):
        self._father = father
        self._son = son

class LogicalDataType:
    CHARACTER = 0
    VARCHAR = 1
    BIT = 2
    VARBIT = 3
    NUMERIC = 4
    DECIMAL = 5
    INTEGER = 6
    SMALLINT = 7
    FLOAT = 8
    REAL = 9
    DOUBLE = 10
    DATE = 11
    TIME = 12
    TIMESTAMP = 13
    INTERVAL = 14

    def to_string(cls, type):
        pass
    to_string = classmethod(to_string) #transforma el metodo to_string en estatico

    def get_description(cls, type):
        pass

    get_description = classmethod(get_description)

class Label(RectBase):
    def __init__(self, text):
        self._text = ""

    def set_text(self, text):
        pass

    def get_text(self):
        pass


class Rectangle(RectBase):
    def __init__(self, x, y):
        self.set_x = x
        self.set_y = y

