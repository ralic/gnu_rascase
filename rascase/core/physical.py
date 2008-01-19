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

import rascase.core.base as base

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
