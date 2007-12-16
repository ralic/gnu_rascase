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

import gtk
import gtk.glade
from pkg_resources import resource_string

class ControlMainWindow:
    def __init__(self):
        self.gladefile = "/home/freyes/Projects/rascase.git/rascase/resources/glade/wndmain.glade"
        self.gladewin = gtk.glade.XML(self.gladefile)
        signals_dic = {"on_wndmain_delete":gtk.main_quit}
        self.gladewin.signal_autoconnect(signals_dic)
        aux = self.gladewin.get_widget("vbox_main")
        self.win = self.gladewin.get_widget("wndmain")
        if aux is None:
            print 'aux es none'

        uimanager = gtk.UIManager()
        accelgroup = uimanager.get_accel_group()
        self.win.add_accel_group(accelgroup)
        action_group = gtk.ActionGroup('my_actions')
        action_group.add_actions([
            ('NewModel', gtk.STOCK_NEW, None, '<Control>n', 'Crea un nuevo modelo', 
             self.new_model),])
        uimanager.insert_action_group(action_group, 0)
        uimanager.add_ui_from_file("/home/freyes/Projects/rascase.git/rascase/resources/uidefs/toolbar.xml")

        menubar = uimanager.get_widget("/Menubar")
        aux.pack_start(menubar)

        toolbar = uimanager.get_widget("/Toolbar")
        aux.pack_start(toolbar)

        self.win.show_all()
        gtk.main()

    def new_model(self):
        pass

