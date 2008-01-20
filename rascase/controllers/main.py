# -*- coding: utf-8 -*-
##
## main.py
## Login : <freyes@yoda.>
## Started on  Fri Dec 14 23:03:32 2007 Felipe Reyes
## $Id$
## 
## Copyright (C) 2007 Felipe Reyes
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

# importa los modulos del sistema
import sys
import gtk
import gtk.glade
from pkg_resources import resource_string

# importa los modulos locales
from rascase.views import main


def start():
    """
    Esta función es solo para inicializar la aplicación
    """
    # this function code was taken from exaile <http://www.exaile.org>
    if sys.platform == 'linux2':
        # Set process name.  Only works on Linux >= 2.1.57.
        try:
            import dl
            libc = dl.open('/lib/libc.so.6')
            libc.call('prctl', 15, 'rascase\0', 0, 0, 0) # 15 is PR_SET_NAME
        except:
            pass
    # end exaile code
    ControlMainWindow()

class ControlMainWindow:
    def __init__(self):
        from pkg_resources import resource_string
        resource_string('rascase.resources.glade', 'wndmain.glade')
        self.viewmain = main.ViewMainWindow(self)
        gtk.main()
            
    def new_model(self):
        pass

