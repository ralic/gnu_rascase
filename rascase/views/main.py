# coding=utf-8
"""Módulo que contiene las principales clases vista

"""
##
## main.py
## Login : <freyes@yoda.>
## Started on  Sun Dec 16 16:17:45 2007 Felipe Reyes
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

import gobject
import gtk
import gtk.glade
import goocanvas


from rascase.views import components

class ViewMainWindow:
    """Vista principal

    En esta vista se despliegan los elementos más importantes del software como el canvas, la barra de herramientas y de menu, entre otros

    """
    def __init__(self,control):
        self.control = control #control que es dueño de la vista
        self.gladefile = "/home/freyes/Projects/rascase.git/rascase/resources/glade/wndmain.glade"
        self.wTree = gtk.glade.XML(self.gladefile)
        signals_dic = {"on_wndmain_delete_event":gtk.main_quit}
        self.wTree.signal_autoconnect(signals_dic)

        # hace las paginas del GtkNotebook
        self.ntbk_main = self.wTree.get_widget("ntbk_main")
        self.canvas = [None]
        self.canvas[0] = components.Canvas()
        
        #item = components.EntityComponent(0,40)
        #self.canvas[0].add_child(item)

        #item = components.EntityComponent(50,50)

        #hijo = goocanvas.Text(text="atributo 1\tP")
        #hijo = components.AttributeComponent("atributo 1")
        #item.add_attribute(hijo)

        #hijo = goocanvas.Text(text="atributo 2")
        #item.add_attribute(hijo)

        #hijo = goocanvas.Text(text="atributo 3")
        #item.add_attribute(hijo)
        
        #self.canvas[0].add_child(item)
        
        container = gtk.HBox()
        widget = gtk.Label("ejemplo.rxl")
        container.pack_start(widget)

        widget = gtk.Button()
        imagen = gtk.Image()
        imagen.set_from_stock(gtk.STOCK_CLOSE,gtk.ICON_SIZE_BUTTON)
        widget.add(imagen)
        container.pack_start(widget)
        
        container.show_all()

        self.ntbk_main.append_page(self.canvas[0].scrolled_win,container)
        
        self.canvas.append(components.Canvas())
        container = gtk.HBox()
        widget = gtk.Label("ejemplo2.rxl")
        container.pack_start(widget)

        widget = gtk.Button()
        imagen = gtk.Image()
        imagen.set_from_stock(gtk.STOCK_CLOSE,gtk.ICON_SIZE_BUTTON)
        widget.add(imagen)
        container.pack_start(widget)
        
        container.show_all()
        print self.canvas[1]
        self.ntbk_main.append_page(self.canvas[1].scrolled_win,container)

        
        # se ponen los archivos en el files_list

        files_list = self.wTree.get_widget("files_list")
        files_list_model = gtk.ListStore(gobject.TYPE_STRING)
        
        files_list_model.append(["ejemplo.rxl"])
        files_list_model.append(["ejemplo2.rxl"])
        files_list_model.append(["webshop.rxl"])
        files_list_model.append(["libreria.rxl"])
        

        files_list.set_model(files_list_model)

        tvcol = gtk.TreeViewColumn("Modelo")
        files_list.append_column(tvcol)
        cell = gtk.CellRendererText()
        tvcol.pack_start(cell)
        tvcol.add_attribute(cell, 'text', 0)
        

        # the properties of the window were defined
        self.win = self.wTree.get_widget("wndmain")
        self.win.set_default_size(600,500)
        self.win.set_title("RasCASE")
        if self.win is None:
            print "self.win es none"

        self.win.show_all()
