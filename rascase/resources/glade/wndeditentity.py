##
## wndeditentity.py
## Login : <freyes@yoda.>
## Started on  Tue Dec 18 18:57:08 2007 Felipe Reyes
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


def main():
    wTree = gtk.glade.XML("wndeditentity.glade")

    files_list = wTree.get_widget("tree_attributes")
    files_list_model = gtk.ListStore(gobject.TYPE_STRING,
                                     gobject.TYPE_STRING,
                                     gobject.TYPE_STRING,
                                     gobject.TYPE_BOOLEAN)
    
    files_list_model.append(("P", "id_factura", "INT", True))
    files_list_model.append((" ", "fecha", "TIMESTAMP", False))
        

    files_list.set_model(files_list_model)

    tvcol = gtk.TreeViewColumn("PI")
    files_list.append_column(tvcol)
    cell = gtk.CellRendererText()
    tvcol.pack_start(cell)
    tvcol.add_attribute(cell, 'text', 0)
    
    tvcol = gtk.TreeViewColumn("nombre")
    files_list.append_column(tvcol)
    cell = gtk.CellRendererText()
    tvcol.pack_start(cell)
    tvcol.add_attribute(cell, 'text', 1)

    tvcol = gtk.TreeViewColumn("tipo de dato")
    files_list.append_column(tvcol)
    cell = gtk.CellRendererText()
    tvcol.pack_start(cell)
    tvcol.add_attribute(cell, 'text', 2)

    tvcol = gtk.TreeViewColumn("M")
    files_list.append_column(tvcol)
    cell = gtk.CellRendererToggle()
    tvcol.pack_start(cell)
    tvcol.add_attribute(cell, 'active', 3)

    win = wTree.get_widget("wndeditentity")
    win.set_title("Editar Entidad")
    win.show_all()
    gtk.main()

if __name__ == "__main__":
    main()
