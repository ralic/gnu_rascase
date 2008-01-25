# coding=utf-8
##
## logical.py
## Login : <freyes@yoda>
## Started on  Mon Jan 21 15:55:21 2008 Felipe Reyes
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

class ControlEditEntity:
    def __init__(self, entity):
        self._entity = entity

    def save(self):
        pass

class ControlEditLabel:
    def __init__(self, label):
        self._label = label

    def save_text(self, text):
        pass

class ControlEditRectangle:
    def __init__(self, rectangle):
        pass

    def save(self):
        pass

    
