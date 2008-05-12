# -*- coding: utf-8 -*-
"""
Este modulo contiene toda la implementación relacionada al sistema de plugins de la herramienta

"""
##
## plugins.py
## Login : <freyes@yoda>
## Started on  Sun Jan 20 17:04:17 2008 Felipe Reyes
## $Id$
##
## Copyright (C) 2008 Felipe Reyes <felipereyes@gmail.com>
##
## This file is part of Rascase.
##
## Rascase is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## Rascase is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.
##

class PluginManager:
    def __init__(self):
        pass

    def get_datadict_plugins(self):
        pass

    def get_script_plugins(self):
        pass

class IPluginScriptGenerator:
    def __init__(self):
        self._name = None
        self._version = None
        self._description = None
        self._author = None

    def initialize(self):
        raise NotImplemented

    def configure(self):
        raise NotImplemented

    def create_table(self, name, description):
        raise NotImplemented

    def create_reference(self, name, description, orig, dest):
        raise NotImplemented

    def finalize(self):
        raise NotImplemented

class IPluginDataDictGenerator:
    def __init__(self):
        self._name = None
        self._version = None
        self._description = None
        self._author = None

    def initialize(self):
        raise NotImplemented

    def configure(self):
        raise NotImplemented

    def create_table(self, name, description):
        raise NotImplemented

    def create_column(self, name, description, datatype, default_value, primary, mandatory):
        raise NotImplemented

    def create_reference(self, name, description, orig, dest):
        raise NotImplemented

    def finalize(self):
        raise NotImplemented

    
    

    
