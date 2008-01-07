##
## wndeditreference.py
## Login : <freyes@yoda.>
## Started on  Tue Dec 18 19:32:42 2007 Felipe Reyes
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
    wTree = gtk.glade.XML("wndeditreference.glade")


    win = wTree.get_widget("wndeditreference")
    win.set_title("Editar Referencia")
    win.show_all()
    gtk.main()

if __name__ == "__main__":
    main()