# -*- coding: utf-8 -*-
"""
Este modulo contiene las clases relacionadas con la implementación de las funcionalidades a nivel de modelo para la gestión de 'modelos físicos'

"""
##
## physical.py
## Login : <freyes@yoda>
## Started on  Sat Jan 19 17:03:09 2008 Felipe Reyes
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

class PhysicalBase:
    def __init__(self):
        self._name = None
        self._codename = None
        self._description = None

    def set_name(self, name):
        pass

    def get_name(self):
        pass

    def set_codename(self, codename):
        pass

    def get_codename(self):
        pass

    def set_description(self, description):
        pass

    def check(self):
        pass

    


class PhysicalModel(base.ModelBase):
    def __init__(self, logicalmodel, path=None):
        self._script_plugin = None
        self._dict_plugin = None
        self._tables_list = None
        self._references = None

    def generate_script(self, path=None):
        return False

    def generate_dictionary(self, path=None):
        return False

    def set_script_plugin(self, plugin):
        pass

    def get_script_plugin(self):
        return self._script_plugin

    def set_dict_plugin(self, plugin):
        pass

    def get_dict_plugin(self):
        return self._dict_plugin

class Table:
    def __init__(self):
        self._columns_list = None

    def add_column(self, column):
        pass

    def del_column(self, column):
        pass

class Column(PhysicalBase):
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

class Reference:
    def __init__(self, table1, table2):
        self._table1 = table1
        self._table2 = table2

    def set_table1(self, table):
        pass

    def get_table1(self, table):
        pass

    def set_table2(self, table):
        pass

class PhysicalDataType:
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
