# -*- coding: utf-8 -*-
"""
En este modulo se encuentran las clases base de la capa modelo del paradigma MVC++

"""
##
## main.py
## Login : <freyes@yoda>
## Started on  Sat Jan 19 16:24:12 2008 Felipe Reyes
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

import gconf

class ModelBase:
    def __init__(self):
        self._name = None
        self._path = None

    def save(self, path=None):
        return False

    def print_model(self):
        return False

    def export_to_png(self):
        return False

    def check(self):
        return None #retorna una lista de errores

class ConfigurationManager:
    def __init__(self):
        self._client = gconf.client_get_default()
        self._client.add_dir('/apps/rascase', gconf.CLIENT_PRELOAD_NONE)

    def get_entity_color(self):
        res = self._client.get_string('/apps/rascase/entity_color')
        print 'entity_color: ', res
        return res

    def set_entity_color(self, value):
        self._client.set_string('/apps/rascase/entity_color', value)

    def add_recently_opened(self,path):
        pass

    def set_label_color(self, value):
        self._client.set_string('/apps/rascase/label_color', value)

    def get_label_color(self):
        return self._client.get_label_color('/apps/rascase/label_color')

    def set_relationship_color(self, value):
        self._client.set_string('/apps/rascase/relationship_color', value)

    def get_relationship_color(self):
        return self._client.get_string('/apps/rascase/relationship_color')

    def set_table_color(self, value):
        self._client.set_string('/apps/rascase/table_color', value)

    def get_table_color(self):
        return self._client.get_string('/apps/rascase/table_color')

    def set_reference_color(self, value):
        self._client.set_string('/apps/rascase/reference_color', value)

    def get_reference_color(self):
        return self._client.get_string('/apps/rascase/reference_color')

    def set_inheritance_color(self, value):
        self._client.set_string('/apps/rascase/inheritance_color', value)

    def get_inheritance_color(self):
        return self._client.get_string('/apps/rascase/inheritance_color')

    def set_last_project_opened(self, path):
        self._client.set_string('/apps/rascase/last_project', value)

    def get_last_project_opened(self):
        return self._client.get_string('/apps/rascase/last_project')
    

    
    

    
