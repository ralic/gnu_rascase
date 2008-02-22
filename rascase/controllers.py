# -*- coding: utf-8 -*-
##
## controllers.py
## Login : <freyes@yoda>
## Started on  Tue Feb 12 11:59:58 2008 Felipe Reyes
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

import sys
import logging
import gtk
import gtk.glade
from pkg_resources import resource_filename

# importa los modulos locales
from rascase.views import *
from rascase.core import *

def start():
    """
    Esta función es solo para inicializar la aplicación y no debe ser utilizada,
    salvo por el script generado por setuptools

    """
    # this code was taken from exaile <http://www.exaile.org>
    if sys.platform == 'linux2':
        # Set process name.  Only works on Linux >= 2.1.57.
        try:
            import dl
            libc = dl.open('/lib/libc.so.6')
            libc.call('prctl', 15, 'rascase\0', 0, 0, 0) # 15 is PR_SET_NAME
        except:
            pass
    # end exaile code

    #setup the logging system

    # code adapted from
    # http://docs.python.org/lib/multiple-destinations.html example
    # set up logging to file - see previous section for more details
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M')
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)

    # Now, define a couple of other loggers which might represent areas in your
    # application:

    log = logging.getLogger('controllers')
    log.info('Starting the application')

    ControlMainWindow()

class ControlEntityComponent:
    def __init__(self, model):
        """Construye un controlador para que gestione una instancia de EntityComponent (la vista)
        y una instancia de Entity (modelo)

        """
        self._view = EntityComponent(model.get_x(),
                                     model.get_y(),
                                     model.get_linecolor(),
                                     model.get_color())

        for attribute in model.get_attributes():
            view_attr = goocanvas.Table(can_focus = False)

            txt = goocanvas.Text(parent=view_attr,
                                 text=attribute.get_name())
            view_attr.set_child_properties(txt, row=0, column=0)

#            txt = goocanvas.Text(parent=view_attr,
#                                 text=attribute.get_

            self._view.add_attribute(view_attr)


class ControlAttributeComponent:
    def __init__(self):
        pass

class ControlRelationshipComponent:
    def __init__(self):
        pass

class ControlInheritanceComponent:
    def __init__(self):
        pass

class ControlTableComponent:
    def __init__(self):
        pass

class ControlReferenceComponent:
    def __init__(self):
        pass

class ControlRectangleComponent:
    def __init__(self):
        pass

class ControlLabelComponent:
    def __init__(self):
        pass

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

class ControlMainWindow:
    def __init__(self):
        self._project = None

        self._view = ViewMainWindow(control=self)
        gtk.main()

    def main(self):
        pass

    def create_new_project(self):
        """Se encarga de crear un nuevo proyecto y retorna una lista con
        los path de los modelos que estan asociados al proyecto

        """
        self._project = Project()
        lista = list()
        modelos = self._project.get_models()
        for x in range(len(modelos)):
            lista.append(modelos.pop(x).get_path())

        return lista

    def create_new_logical_model(self):
        pass

    def generate_physical_model(self, logicalmodel):
        pass

    def open_project(self, path):

        aux_path = path

        #define the filter applied to the file chooser dialog
        filtro = gtk.FileFilter()
        filtro.add_pattern("*.rprj")
        filtro.set_name("Proyecto")

        if aux_path==None:
            controlopenfile = ControlSaveFileDialog(action=gtk.FILE_CHOOSER_ACTION_OPEN,
                                                    title="Abir Proyecto",
                                                    parent=self._view.get_window(),
                                                    filter=filtro)
            aux_path = controlopenfile.get_path() #obtain the path selected by the user

        self._project = Project(aux_path)

        aux = list()
        for elem in self._project.get_models():
            aux.append(elem.get_path())

        return aux

    def open_logical_model(self, path):
        pass

    def open_physical_model(self, path):
        pass

    def close_project(self):
        pass

    def close_model(self, model):
        pass

    def add_entity(self, model, x, y):
        pass

    def add_relationship(self, model, entity1, entity2):
        pass

    def add_inheritance(self, model, father, son):
        pass

    def add_label(self, model, x, y, width, height):
        pass

    def add_rectangle(self, model, x, y, width, height):
        pass

    def edit_entity(self, entity):
        pass

    def edit_relationship(self, relationship):
        pass

    def edit_inheritance(self, inheritance):
        pass

    def edit_label(self, label):
        pass

    def edit_rectangle(self, rectangle):
        pass

    def delete_entity(self, entity):
        pass

    def delete_relationship(self, relationship):
        pass

    def delete_inheritance(self, inheritance):
        pass

    def delete_label(self, label):
        pass

    def delete_rectangle(self, rectangle):
        pass

    def edit_table(self, table):
        pass

    def edit_reference(self, reference):
        pass

    def print_model(self, model):
        pass

    def export_model(self, model):
        pass

    def new_model(self):
        pass

    def quit(self):
        log = logging.getLogger('controllers')
        log.info("Quiting...")
        gtk.main_quit()

class ControlSaveFileDialog:
    def __init__(self, action, project=None, model=None, title=None, parent=None, filter=None):

        self._path = None
        self._view = ViewFileDialog(action=action, title=title, parent=parent, filter=filter)

        self.set_path(self._view.path)
        log.debug("Path: %s", self._path)

    def save(self, filename):
        pass

    def get_path(self):
        return self._path

    def set_path(self, path):
        self._path = path

if __name__=="__main__":
    start()
