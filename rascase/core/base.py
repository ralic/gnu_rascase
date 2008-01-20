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

