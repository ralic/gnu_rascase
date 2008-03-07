# -*- coding: utf-8 -*-
##
## controllers.py
## Login : <freyes@yoda>
## Started on  Tue Feb 12 11:59:58 2008 Felipe Reyes
## $Id$
##
## Copyright (C) 2008 Felipe Reyes <felipereyes@gmail.com>
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
## Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
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
                        #format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        format='%(levelname)-8s %(message)s',
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

log = logging.getLogger('controllers')

class ControlEntityComponent:
    def __init__(self, entity_model):
        """Construye un controlador para que gestione una instancia de EntityComponent (la vista)
        y una instancia de Entity (modelo)

        """
        log.debug("Constructing a ControlEntityComponent")

        self._entity_model = entity_model
        self._view = EntityComponent(entity_model.get_name(),
                                     entity_model.get_x(),
                                     entity_model.get_y(),
                                     entity_model.get_width(),
                                     entity_model.get_height())

        self._view.set_fillcolor(self._entity_model.get_fillcolor())
        self._view.set_linecolor(self._entity_model.get_linecolor())

        for attribute in entity_model.get_attributes():

            view_attr = AttributeComponent(name=attribute.get_name(),
                                           datatype=attribute.get_data_type(),
                                           default_value=attribute.get_default_value(),
                                           pk=attribute.is_primary_key(),
                                           mandatory=attribute.is_mandatory())

            self._view.add_attribute(view_attr)
            view_attr.set_data("model", attribute)

        self._view.connect("on-double-click", self._on_edit_selected)
        self._view.connect("on-movement", self._on_movement)
        self._view.connect("changed-dimensions", self._on_changed_dimensions)

    def add_attribute(self, attribute_model=None):
        if attribute_model == None:
            attr = Attribute()
        else:
            attr = attribute_model

        self._entity_model.add_attribute(attr)

        attr_comp = AttributeComponent(attr.get_name(),
                                         attr.get_codename(),
                                         attr.get_default_value(),
                                         attr.is_primary_key(),
                                         attr.is_mandatory())
        attr_comp.set_data("model", attr)

        self._view.add_attribute(attr_comp)

        return attr

    def _on_edit_selected(self,item):
        "Este metodo es llamado por la vista cuando el usuario seleccionar editar la entidad"

        parent = item.get_canvas().get_toplevel()
        ControlEditEntity(self._entity_model, control=self, parent=parent)

    def refresh(self):
        self._view.set_title(self._entity_model.get_name())
        self._view.refresh()
        print self._view.attr_list
        for attr in self._view.attr_list:
            attr.refresh()

    def _on_movement(self, item):
        new_x = item.get_x()
        new_y = item.get_y()

        self._entity_model.set_x(float(new_x))
        self._entity_model.set_y(float(new_y))

    def _on_changed_dimensions(self, item):

        new_height = float(item.get_height())
        new_width = float(item.get_width())

        self._entity_model.set_height(new_height)
        self._entity_model.set_width(new_width)

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
    def __init__(self, entity, control, parent):
        self._entity = entity
        self._control = control

        self._view = ViewEditEntity(self._entity, self, parent=parent)

    def get_new_attribute(self):
        attr = self._control.add_attribute()
        return attr

    def logical_data_type_to_string(self, datatype):
        return LogicalDataType.to_string(datatype)

    def refresh(self):
        self._control.refresh()


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

        filtro = gtk.FileFilter()
        filtro.add_pattern("*.rprj")
        filtro.set_name("Proyecto")

        filedialog = ControlSaveFileDialog(action=gtk.FILE_CHOOSER_ACTION_SAVE,
                                           title="Gardar nuevo proyecto",
                                           parent=self._view.get_window(),
                                           filter=filtro)
        aux_path = filedialog.get_path()
        if aux_path == None:
            return None

        self._project = Project()
        self._project.save(aux_path)
        lista = list()
        modelos = self._project.get_models()
        for x in range(len(modelos)):
            lista.append(modelos.pop(x).get_path())

        return lista

    def create_new_logical_model(self):

        filtro = gtk.FileFilter()
        filtro.add_pattern("*.rxl")
        filtro.set_name("Modelo Lógico")

        filedialog = ControlSaveFileDialog(action=gtk.FILE_CHOOSER_ACTION_SAVE,
                                           title="Gardar nuevo proyecto",
                                           parent=self._view.get_window(),
                                           filter=filtro)
        aux_path = filedialog.get_path()
        if aux_path == None:
            log.debug("The user did not selected a path for the new logical model")
            return None

        logical_model = LogicalModel()
        logical_model.save(aux_path)
        self._project.add_model(logical_model)

        return self._project.get_models()

    def construct_model(self, filename):

        model = self._project.get_model(filename)

        if isinstance(model, LogicalModel):
            return self._construct_logical_model(model)
        elif isinstance(model, PhysicalModel):
            return self._construct_physical_model(model)
        else:
            log.debug("Could not match the type of the instance %s", model)
            return None

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

        return self._project.get_models()

    def save_project(self):
        "Almacena el proyecto"
        return self._project.save()

    def save_model(self, modelpath, new_modelpath=None):
        """Almancena el modelo identificado por modelpath, en caso de que new_modelpath sea distinto de None
        se almacena el model identificado por modelpath en la nueva ruta definida por new_modelpath"""

        model = self._project.get_model(modelpath)
        if model == None:
            log.debug("Trying to save a non existing model")
            return False

        if new_modelpath != None:
            model.save(new_modelpath)
        else:
            model.save()

    def open_logical_model(self, path):
        pass

    def open_physical_model(self, path):
        pass

    def close_project(self):
        pass

    def close_model(self, model):
        pass

    def add_entity(self, x, y, modelpath):
        logical_model = self._project.get_model(modelpath)
        entity_model = Entity()
        logical_model.add_entity(entity_model)
        entity_control = ControlEntityComponent(entity_model)

        return entity_control._view

    def add_relationship(self, modelpath, entity1, entity2, cardinality, name, codename, description):
        model = self._project.get_model(modelpath)

        relationship = Relationship(entity1=entity1, entity2=entity2)

        relationship.set_cardinality(cardinality)
        relationship.set_name(name)
        relationship.set_codename(codename)
        relationship.set_description(description)

        model.add_relationship(relationship)

        ControlRelationshipComponent(relationship)

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

    def get_all_entities(self, modelpath):
        model = self._project.get_model(modelpath)

        aux_list = list()
        for entity in model.get_all_entities():
            aux_list.append((entity.get_name(), entity.get_codename()))

        return aux_list

    def quit(self):
        log = logging.getLogger('controllers')
        log.info("Quiting...")
        gtk.main_quit()

    def _construct_logical_model(self, logical_model):
        "Construye el canvas y todos los componentes con sus respectivos controladores"

        canvas = Canvas()

        for entity in logical_model.get_all_entities():
            aux_item = ControlEntityComponent(entity)
            canvas.add_child(aux_item._view)

        for relationship in logical_model.get_all_relationships():
            aux_item = ControlRelationshipComponent(relationship)
            canvas.add_child(aux_item._view)

        for inheritance in logical_model.get_all_inheritances():
            aux_item = ControlInheritanceComponent(inheritance)
            canvas.add_child(aux_item._view)

        return canvas

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
