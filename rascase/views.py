# coding=utf-8
##
## base.py
## Login : <freyes@yoda>
## Started on  Tue Jan 22 11:29:49 2008 Felipe Reyes
## $Id$
##
## Copyright (C) 2008 Felipe Reyes <felipereyes@gmail.com>
##
## This file is part of Rascase.
##
## Rascase is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## Rascase is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.
##

import gobject
import gtk
import gtk.glade
import goocanvas
import cairo
import pangocairo
import pango
import os
import math
from color import *
##logging system
import logging
log = logging.getLogger('views')
##

from pkg_resources import resource_filename

class ViewEditEntity:
    def __init__(self, entity, control, parent):

        self._control = control
        self._entity = entity

        glade_file = resource_filename("rascase.resources.glade", "wndeditentity.glade")
        self._wTree = gtk.glade.XML(glade_file)

        signals_dic = {"on_btn_ok_clicked":self._on_btn_ok_clicked,
                       "on_btn_cancel_clicked":self._on_btn_cancel_clicked,
                       "on_new_attr_clicked":self._on_new_attr_clicked}

        self._wTree.signal_autoconnect(signals_dic)
        self._window = self._wTree.get_widget("wndeditentity")
        self._window.set_transient_for(parent)

        ## main information
        widget = self._wTree.get_widget("entry_name")
        widget.set_text(entity.get_name())

        widget = self._wTree.get_widget("entry_codename")
        widget.set_text(entity.get_codename())

        widget = self._wTree.get_widget("txt_description")
        buff = widget.get_buffer()
        buff.set_text(entity.get_description())

        ## attributes
        tree_attributes = self._wTree.get_widget("tree_attributes")

        self._attr_list = gtk.ListStore(gobject.TYPE_STRING, #0 name
                                        gobject.TYPE_STRING, #1 codename
                                        gobject.TYPE_INT,    #2 datatype constant
                                        gobject.TYPE_STRING, #3 datatype string
                                        gobject.TYPE_OBJECT, #4 all data_types
                                        gobject.TYPE_INT,    #5 data_type_length
                                        gobject.TYPE_BOOLEAN,#6 pk
                                        gobject.TYPE_BOOLEAN,#7 mandatory
                                        gobject.TYPE_STRING, #8 description
                                        object)              #9 el objeto atributo

        self._datatypes_store = gtk.ListStore(gobject.TYPE_STRING,# 0 datatype NAME
                                              gobject.TYPE_INT)   # 1 datatype CODE

        from rascase.core import LogicalDataType
        for dt in LogicalDataType.get_data_types():
            self._datatypes_store.append([LogicalDataType.to_string(dt), dt])

        for attr in self._entity.get_attributes():

            if len(attr.get_data_type()) > 1:
                dt_length = int(attr.get_data_type()[1])
            else:
                dt_length = int(0)

            self._attr_list.append([str(attr.get_name()),
                                    str(attr.get_codename()),
                                    int(attr.get_data_type()[0]),
                                    str(LogicalDataType.to_string(attr.get_data_type()[0])),
                                    self._datatypes_store,
                                    dt_length,
                                    attr.is_primary_key(),
                                    attr.is_mandatory(),
                                    attr.get_description(),
                                    attr])

        tree_attributes.set_model(self._attr_list)

        # column name
        col_name = gtk.TreeViewColumn("Nombre")
        tree_attributes.append_column(col_name)
        cell = gtk.CellRendererText()
        cell.set_property("editable", True)
        cell.connect("edited", self._on_name_edited)
        col_name.pack_start(cell)
        col_name.add_attribute(cell, "text", 0)

        #column codename
        col_codename = gtk.TreeViewColumn("Código")
        tree_attributes.append_column(col_codename)
        cell = gtk.CellRendererText()
        cell.set_property("editable", True)
        cell.connect("edited", self._on_codename_edited)
        col_codename.pack_start(cell)
        col_codename.add_attribute(cell, "text", 1)

        # data type ?? por el momento no lo ponemos
        cell = gtk.CellRendererCombo()
        cell.set_property("model",self._datatypes_store)
        cell.set_property("has-entry", False)
        cell.set_property("text-column", 0)#de donde sacar el texto para el combo
        cell.set_property("editable", True)
        cell.connect("edited", self._on_data_type_edited)
        col_datatype = gtk.TreeViewColumn("Tipo de dato", cell)
        col_datatype.set_attributes(cell, text=3)
        tree_attributes.append_column(col_datatype)
        #datatype length
        cell = gtk.CellRendererText()
        cell.set_property("editable", True)
        cell.connect("edited", self._on_data_type_length)
        col_datatype.pack_start(cell)
        col_datatype.add_attribute(cell, "text", 5)


        #pk
        cell = gtk.CellRendererToggle()
        cell.set_property("activatable", True)
        cell.connect("toggled", self._on_pk_togled)
        col = gtk.TreeViewColumn("Identificador", cell)
        col.set_attributes(cell, active=6)
        tree_attributes.append_column(col)

        #mandatory
        cell = gtk.CellRendererToggle()
        cell.set_property("activatable", True)
        cell.connect("toggled", self._on_mandatory_togled)
        col = gtk.TreeViewColumn("Obligatorio", cell)
        col.set_attributes(cell, active=7)
        tree_attributes.append_column(col)

        # column name
        col_name = gtk.TreeViewColumn("Descripción")
        tree_attributes.append_column(col_name)
        cell = gtk.CellRendererText()
        cell.set_property("editable", True)
        cell.connect("edited", self._on_description_edited)
        col_name.pack_start(cell)
        col_name.add_attribute(cell, "text", 8)

        self._window.show_all()

    #signals
    def _on_name_edited(self, cellrenderertext, path, new_text):
        iter_ = self._attr_list.get_iter(path)

        attr = self._attr_list.get_value(iter_, 9)

        attr.set_name(new_text)
        self._attr_list.set_value(iter_, 0, attr.get_name())

        attr.set_codename(new_text)
        self._attr_list.set_value(iter_, 1, attr.get_codename())

    def _on_codename_edited(self, cellrenderertext, path, new_text):
        iter_ = self._attr_list.get_iter(path)

        attr = self._attr_list.get_value(iter_, 9)
        attr.set_codename(new_text)

        self._attr_list.set_value(iter_, 1, attr.get_codename())

    def _on_data_type_edited(self, cellrenderertext, path, new_text):

        iter_ = self._datatypes_store.get_iter_first()
        while iter_ != None:

            value = self._datatypes_store.get_value(iter_, 0)

            if value == new_text:
                iter_2 = self._attr_list.get_iter(path)

                # TODO: debe actualizarse el object
                attr = self._attr_list.get_value(iter_2, 9)
                attr.set_data_type(self._datatypes_store.get_value(iter_, 1),
                                   self._attr_list.get_value(iter_2, 5))

                self._attr_list.set(iter_2, 2, self._datatypes_store.get_value(iter_, 1))
                self._attr_list.set(iter_2, 3, value)
                break

            iter_ = self._datatypes_store.iter_next(iter_)

    def _on_data_type_length(self, cellrenderertext, path, new_text):

        #if try to put a nondigit string in the entry
        if not new_text.isdigit():
            dialog = gtk.Dialog("Largo no valido",
                     self._window,
                     gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                     (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
            hbox = gtk.HBox()

            image = gtk.Image()
            image.set_from_stock(gtk.STOCK_DIALOG_INFO, gtk.ICON_SIZE_DIALOG)
            hbox.pack_start(image)

            label = gtk.Label("El largo de un tipo de dato debe ser numérico")
            hbox.pack_start(label)

            hbox.show_all()
            dialog.vbox.pack_start(hbox)
            dialog.run()
            dialog.destroy()
            return

        iter_ = self._attr_list.get_iter(path)

        attr = self._attr_list.get_value(iter_, 9)
        attr.set_data_type(None, int(new_text))

        if len(attr.get_data_type()) > 1:
            self._attr_list.set(iter_, 5, int(attr.get_data_type()[1]))
        else:
            self._attr_list.set(iter_, 5, 0)

    def _on_pk_togled(self, cellrenderertoggle, path):

        iter_attr_list = self._attr_list.get_iter(path)

        attr = self._attr_list.get_value(iter_attr_list, 9)
        attr.set_primary_key(not attr.is_primary_key())
        self._attr_list.set_value(iter_attr_list, 6, attr.is_primary_key())

    def _on_mandatory_togled(self, cellrenderertoggle, path):

        iter_attr_list = self._attr_list.get_iter(path)

        attr = self._attr_list.get_value(iter_attr_list, 9)
        attr.set_mandatory(not attr.is_mandatory())
        self._attr_list.set_value(iter_attr_list, 7, attr.is_mandatory())

    def _on_description_edited(self, cellrenderertext, path, new_text):
        iter_ = self._attr_list.get_iter(path)

        attr = self._attr_list.get_value(iter_, 9)
        attr.set_description(new_text)

        self._attr_list.set_value(iter_, 8, attr.get_description())

    def _on_new_attr_clicked(self, toolbutton):
        attr = self._control.get_new_attribute()

        #para saber si tiene datatype length
        if len(attr.get_data_type()) > 1:
            dt_length = attr.get_data_type()[1]
        else:
            dt_length = 0

        self._attr_list.append([attr.get_name(),
                                attr.get_codename(),
                                attr.get_data_type()[0],
                                self._control.logical_data_type_to_string(attr.get_data_type()[0]),
                                self._datatypes_store,
                                dt_length,
                                attr.is_primary_key(),
                                attr.is_mandatory(),
                                attr.get_description(),
                                attr])

    def _on_btn_ok_clicked(self, button):

        widget = self._wTree.get_widget("entry_name")
        self._entity.set_name(widget.get_text())

        widget = self._wTree.get_widget("entry_codename")
        self._entity.set_codename(widget.get_text())

        widget = self._wTree.get_widget("txt_description")
        buff = widget.get_buffer()
        text = buff.get_text(buff.get_start_iter(), buff.get_end_iter())
        self._entity.set_description(text)

        self._control.refresh()
        self._window.destroy()


    def _on_btn_cancel_clicked(self, button):
        pass

    def on_fill_color_set(self, colorbutton):
        pass

    def on_toolbtn_new_attribute(self, toolbutton):
        pass

    def on_toolbtn_cut_attribute(self, toolbutton):
        pass

    def on_toolbtn_copy_attribute(self, toolbutton):
        pass

    def on_toolbtn_paste_attribute(self, toolbutton):
        pass

    def on_toolbtn_delete_attribute(self, toolbutton):
        pass

    def on_primary_toggled(self, checkbutton):
        pass

    def on_mandatory_toggled(self, checkbutton):
        pass

class ViewEditRelationship:
    def __init__(self, relationship, control):
        pass

    def on_dependent1_toggled(self, checkbutton):
        pass

    def on_dependent2_toggled(self, checkbutton):
        pass

    def on_btn_ok_clicked(self, button):
        pass

    def on_btn_cancel_clicked(self, button):
        pass


class ViewEditLabel:
    def __init__(self, label, control):
        pass

    def on_font_set(self, fontbutton):
        pass

    def on_btn_ok_clicked(self, button):
        pass

    def on_btn_cancel_clicked(self, button):
        pass

class ViewEditRectangle:
    def __init__(self, rectangle, control):
        pass

    def on_line_color_set(self, colorbutton):
        pass

    def on_btn_ok_clicked(self, button):
        pass

    def on_btn_cancel_clicked(self, button):
        pass

class ViewFileDialog:
    def __init__(self, action, title, parent, filter):

        self.path = None
        self._window = gtk.FileChooserDialog(action=action,
                                             title=title,
                                             parent=parent,
                                             buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                                                      gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))

        self._window.set_filter(filter)
        self._window.set_property("select-multiple", False)
        self._window.show_all()
        response = self._window.run()

        if response == gtk.RESPONSE_ACCEPT:
            self.path = self._window.get_filename()

        self._window.destroy()

class ViewAddRelationship:
    "Contiene la vista que es desplegada cuando el usuario selecciona agregar una nueva relación"
    def __init__(self, control, parent):

        self._control = control

        entities_list = self._control.get_all_entities()

        self._wTree = gtk.glade.XML(resource_filename('rascase.resources.glade',
                                                      'wndaddrelationship.glade'))

        entry = self._wTree.get_widget("entry_name")
        entry.connect("changed", self._on_entry_name_changed)

        self._window = self._wTree.get_widget("wndaddrelationship")
        self._window.set_transient_for(parent)

        entities_store = gtk.ListStore(gobject.TYPE_STRING, #name
                                       gobject.TYPE_STRING) #codename

        for x in entities_list:
            entities_store.append([x[0],x[1]])

        #combobox for entity 1
        combo = self._wTree.get_widget("combo_entity1")
        combo.set_model(entities_store)
        cell = gtk.CellRendererText()
        combo.pack_start(cell, True)
        combo.add_attribute(cell, 'text', 0)

        #dependent1
        checkbox = self._wTree.get_widget("check1_dependent")
        checkbox.connect("toggled", self._on_check_dependent_toggled)

        #combobox for entity 2
        combo = self._wTree.get_widget("combo_entity2")
        combo.set_model(entities_store)
        cell = gtk.CellRendererText()
        combo.pack_start(cell, True)
        combo.add_attribute(cell, 'text', 0)

        #dependent2
        checkbox = self._wTree.get_widget("check2_dependent")
        checkbox.connect("toggled", self._on_check_dependent_toggled)

        #combox for cardinality types
        cardinalities_store = gtk.ListStore(gobject.TYPE_STRING, #name
                                            gobject.TYPE_INT)    #code

        cardinalities_store.append(['1 a 1', 0])
        cardinalities_store.append(['1 a N', 1])
        cardinalities_store.append(['N a 1', 2])
        cardinalities_store.append(['N a N', 3])

        combo = self._wTree.get_widget("combo_cardinality")
        combo.set_model(cardinalities_store)
        cell = gtk.CellRendererText()
        combo.pack_start(cell)
        combo.add_attribute(cell, 'text', 0)
        combo.connect("changed", self._on_cardinality_changed)

        button = self._wTree.get_widget("btn_cancel")
        button.connect("clicked", self._on_btn_cancel_relationship_clicked)

        button = self._wTree.get_widget("btn_add")
        button.connect("clicked", self._on_btn_add_relationship_clicked)

        self._window.show_all()

    def _on_entry_name_changed(self, entry):
        entry_codename = self._wTree.get_widget("entry_codename")

        aux = entry.get_text().upper().replace(' ', '_')
        entry_codename.set_text(aux)

    def _on_cardinality_changed(self, combobox):
        combo_model = combobox.get_model()
        path_str = str(combobox.get_active())
        iter_cardinality = combo_model.get_iter_from_string(path_str)

        new_value = [combo_model.get_value(iter_cardinality, 0),#name
                     combo_model.get_value(iter_cardinality, 1)]#code (int)

        if new_value[1] == 0: # 1 a 1
            #TODO: configure the dialog when te user selects 1 to 1 relation
            pass

        elif new_value[1] == 1: # 1 a N
            #for entity 1
            checkbox = self._wTree.get_widget("check1_dependent")
            checkbox.set_active(False)
            checkbox.set_sensitive(False)

            checkbox = self._wTree.get_widget("check1_mandatory")
            checkbox.set_sensitive(True)

            #for entity 2
            checkbox = self._wTree.get_widget("check2_dependent")
            checkbox.set_sensitive(True)

            checkbox = self._wTree.get_widget("check2_mandatory")
            checkbox.set_active(True)
            checkbox.set_sensitive(False)


        elif new_value[1] == 2: # N a 1
            #for entity 1
            checkbox = self._wTree.get_widget("check1_dependent")
            checkbox.set_sensitive(True)

            checkbox = self._wTree.get_widget("check1_mandatory")
            checkbox.set_active(True)
            checkbox.set_sensitive(False)

            #for entity 2
            checkbox = self._wTree.get_widget("check2_dependent")
            checkbox.set_active(False)
            checkbox.set_sensitive(False)

            checkbox = self._wTree.get_widget("check2_mandatory")
            checkbox.set_sensitive(True)

        elif new_value[1] == 3: # N a N
            #for entity 1
            checkbox = self._wTree.get_widget("check1_dependent")
            checkbox.set_active(False)
            checkbox.set_sensitive(False)

            checkbox = self._wTree.get_widget("check1_mandatory")
            checkbox.set_sensitive(True)

            #for entity 2
            checkbox = self._wTree.get_widget("check2_dependent")
            checkbox.set_active(False)
            checkbox.set_sensitive(False)

            checkbox = self._wTree.get_widget("check2_mandatory")
            checkbox.set_sensitive(True)

    def _on_check_dependent_toggled(self, togglebutton):
        """Controla la habilitacion y dehabilitacion de los check button
        de la propiedad 'dependiente' para la relación
        """

        if togglebutton == self._wTree.get_widget("check1_dependent"):
            check_dependent = self._wTree.get_widget("check2_dependent")

        elif togglebutton == self._wTree.get_widget("check2_dependent"):
            check_dependent = self._wTree.get_widget("check1_dependent")
        else:
            log.error("Could not be found the checkbutton")
            return

        if togglebutton.get_active():
            check_dependent.set_active(False)
            check_dependent.set_sensitive(False)
        else:
            check_dependent.set_sensitive(True)

    def _on_btn_cancel_relationship_clicked(self, button):
        win = self._wTree.get_widget("wndaddrelationship")

        win.destroy()

    def _on_btn_add_relationship_clicked(self, button):

        # basic information of the relationship
        entry = self._wTree.get_widget("entry_name")
        name = entry.get_text()
        if name == "":
            self._show_dialog("Nombre Relación",
                              "Debe ingresar el nombre de la relación",
                              gtk.STOCK_DIALOG_WARNING)
            return

        entry = self._wTree.get_widget("entry_codename")
        codename = entry.get_text()

        if codename == "":
            self._show_dialog("Codigo Relación",
                              "Debe ingresar el codigo de la relación",
                              gtk.STOCK_DIALOG_WARNING)
            return

        txt = self._wTree.get_widget("txt_description")
        buff = txt.get_buffer()
        description = buff.get_text(buff.get_start_iter(),
                                    buff.get_end_iter())

        ####
        # entity 1
        combo = self._wTree.get_widget("combo_entity1")
        # message if not selected entity 1
        if combo.get_active() == -1:
            self._show_dialog("Seleccione Entidad",
                              "Debe seleccionar las entidades que desea relacionar",
                              gtk.STOCK_DIALOG_WARNING)
            return

        combo_model = combo.get_model()
        iter_combo= combo_model.get_iter_from_string(str(combo.get_active()))

        #get the codename of entity 1
        codename_entity1 = combo_model.get_value(iter_combo, 1)

        check_dependent = self._wTree.get_widget("check1_dependent")
        dependent1 = check_dependent.get_active()

        check_mandatory = self._wTree.get_widget("check1_mandatory")
        mandatory1 = check_mandatory.get_active()

        ####
        # entity 2
        combo = self._wTree.get_widget("combo_entity2")
        # message if not selected entity 2
        if combo.get_active() == -1:
            self._show_dialog("Seleccione Entidad",
                              "Debe seleccionar las entidades que desea relacionar",
                              gtk.STOCK_DIALOG_WARNING)
            return

        iter_combo = combo_model.get_iter_from_string(str(combo.get_active()))
        codename_entity2 = combo_model.get_value(iter_combo, 1)

        check_dependent = self._wTree.get_widget("check2_dependent")
        dependent2 = check_dependent.get_active()

        check_mandatory = self._wTree.get_widget("check2_mandatory")
        mandatory2 = check_mandatory.get_active()

        # cardinality of the relationship
        combo = self._wTree.get_widget("combo_cardinality")
        #message if not selected a cardinality
        if combo.get_active() == -1:
            self._show_dialog("Seleccione Cardinalidad",
                              "Debe seleccionar la cardinalidad para la relación",
                              gtk.STOCK_DIALOG_WARNING)
            return False

        combo_model = combo.get_model()
        iter_combo = combo_model.get_iter_from_string(str(combo.get_active()))

        cardinality = combo_model.get_value(iter_combo, 1)


        answer = self._control.add(name,
                                   codename,
                                   description,
                                   codename_entity1,
                                   dependent1,
                                   mandatory1,
                                   codename_entity2,
                                   dependent2,
                                   mandatory2,
                                   cardinality)

        #message dialog if add_relationsip returns an error
        if not answer:
            self._show_dialog("Relación",
                              """Se ha producido un error inesperado
                              No se pudo agregar la relación""",
                              gtk.STOCK_DIALOG_INFO)
            return False

        self._window.destroy()
        return True

    def _show_dialog(self, title, msg, stock_img):
        dialog = gtk.Dialog(title,
                            self._window,
                            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                            (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        hbox = gtk.HBox()

        image = gtk.Image()
        image.set_from_stock(stock_img , gtk.ICON_SIZE_DIALOG)
        hbox.pack_start(image)

        label = gtk.Label(msg)

        label.set_use_markup(True)
        hbox.pack_start(label)

        hbox.show_all()
        dialog.vbox.pack_start(hbox)
        dialog.run()
        dialog.destroy()
        return

class ViewMainWindow:
    """Vista principal

    En esta vista se despliegan los elementos más importantes del software
    como el canvas, la barra de herramientas y de menu, entre otros.

    """
    def __init__(self,control, file_=None):
        log.info('ViewMainWindow.__init__: file_=%s', file_)
        self._control = control #control que es dueño de la vista
        self.gladefile = resource_filename("rascase.resources.glade", "wndmain.glade")
        self._wTree = gtk.glade.XML(self.gladefile)

        ## widgets
        self._main_toolbar = None
        self._elements_toolbar = None
        self._menubar = None

        ## properties
        self._files_opened = list()
        self._files_list = list()
        self._canvas_list = list()
        self._selected_item = None

        # the association of the signals defined inside glade and the python methods
        signals_dic = {"on_wndmain_delete_event":self._on_delete_main_window,
                       "on_files_list_row_activated":self._on_files_list_row_activated}
        self._wTree.signal_autoconnect(signals_dic)

        # the properties of the window were defined
        self._window = self._wTree.get_widget("wndmain")
        self._window.set_default_size(600,500)
        self._window.set_title("Rascase")

        self._construct_toolbar() # we construct the toolbar

        self._window.show_all()


    # signals

    def _on_delete_main_window(self, widget, event):
        "callback conectado al evento 'delete' de la ventana principal"

        menu_option = self._uimanager.get_widget("/menubar/File/Quit")

        menu_option.activate()
        return True

    def _on_quit_selected(self, menuitem):
        "callback conectado a la opcion salir de la aplicacion"
        dialog = gtk.Dialog("Salir",
                            self._window,
                            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                            (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                             gtk.STOCK_QUIT, gtk.RESPONSE_ACCEPT))

        box = gtk.HBox()

        widget = gtk.Image()
        widget.set_from_stock(gtk.STOCK_QUIT, gtk.ICON_SIZE_DIALOG)
        box.pack_start(widget)

        widget = gtk.Label("¿Desea salir y perder todos los cambios efectuados?")
        box.pack_start(widget)

        box.show_all()
        dialog.vbox.pack_start(box)

        response = dialog.run()
        dialog.destroy()

        if response == gtk.RESPONSE_ACCEPT:
            self._control.quit()

    def _on_new_project(self, menuitem):
        self._files_list = self._control.create_new_project()
        self._reload_files_list()

    def _on_new_model(self, menuitem):
        aux = self._control.create_new_logical_model()
        if aux == None:
            statusbar = self._wTree.get_widget("statusbar")
            context_id = statusbar.get_context_id("Model not created")
            msg_id = statusbar.push(context_id, "Cancelada la creación de un nuevo modelo lógico")
            gobject.timeout_add(10000,self._remove_from_statusbar,context_id, msg_id)
        else:
            print aux
            self._files_list = aux
            self._reload_files_list()

    def _on_open_project(self, menuitem):

        # obtain the list of models associated to the project
        self._files_list = self._control.open_project(path=None)
        self._reload_files_list()

    def _on_save_project(self, menuitem):
        answer = self._control.save_project()
        statusbar = self._wTree.get_widget("statusbar")
        context_id = statusbar.get_context_id("save project")
        if answer:
            msg_id = statusbar.push(context_id, "El proyecto ha sido guardado exitosamente")
        else:
            msg_id = statusbar.push(context_id, "El proyecto no ha podido ser guardado")

        gobject.timeout_add(10000, self._remove_from_statusbar, context_id, msg_id)

    def on_open_model(self, menuitem):
        pass

    def _on_save_model(self, menuitem):
        ntbk = self._wTree.get_widget("ntbk_main")

        child = ntbk.get_nth_page(ntbk.get_current_page())
        canvas = child.get_data("canvas")

        filepath = None
        for x in self._files_opened:
            if x[1] == canvas:
                filepath = x[0]

        if filepath == None:
            log.debug("mmm trying to save a model but could not be found the modelpath")
            return

        self._control.save_model(filepath)

    def on_save_model_as(self, menuitem):
        pass

    def on_add_model_to_project(self, menuitem):
        pass

    def on_remove_model(self, menuitem): #remove the model from the project
        pass

    def on_delete_model(self, menuitem):
        pass

    #on the close of the menu
    def _on_close_file_clicked(self, menuitem):
        ntbk = self._wTree.get_widget("ntbk_main")

        page_num = ntbk.get_current_page()

        #if there is no pages a message is displayed in status bar
        if page_num == -1:
            statusbar = self._wTree.get_widget("statusbar")
            context_id = statusbar.get_context_id("no pages in notebook")
            msg_id = statusbar.push(context_id, "No hay modelo abierto")
            gobject.timeout_add(5000,self._remove_from_statusbar,context_id, msg_id)
            return

        scrolled_win =ntbk.get_nth_page(page_num)

        canvas = scrolled_win.get_data("canvas")
        closed = False
        for i in range(len(self._files_opened)):
            if self._files_opened[i][1] == canvas:
                ntbk.remove_page(page_num)
                del self._files_opened[i]
                break

        statusbar = self._wTree.get_widget("statusbar")
        context_id = statusbar.get_context_id("closing canvas")
        msg_id = statusbar.push(context_id, "Modelo cerrado")
        gobject.timeout_add(5000,self._remove_from_statusbar,context_id, msg_id)


    def _on_add_entity_clicked(self, menuitem):

        ntbk = self._wTree.get_widget("ntbk_main")
        page = ntbk.get_current_page()
        child = ntbk.get_nth_page(page)
        canvas = child.get_data("canvas")

        filepath = None
        for x in self._files_opened:
            if x[1] == canvas:
                filepath = x[0]
                break

        item = self._control.add_entity(0,0, filepath)
        canvas.add_child(item)

    def _on_add_relationship_clicked(self, menuitem):
        self._control.add_relationship()

    def on_add_inheritance_clicked(self, menuitem):
        pass

    def _on_add_label_clicked(self, menuitem):
        #self._control.add_label()
        pass

    def on_add_rectangle_clicked(self,menuitem):
        pass

    #aqui se debe chequear el tipo de componente grafico que se quiere editar
    #para luego hacer la llamada al método correspondiente
    def on_edit_component(self, item, target_item, event):
        pass

    def on_delete_component(self, item, target_item, event):
        pass

    #callbacks usados por el uimanager
    def on_delete_component_clicked(self, menuitem):
        pass

    def on_edit_component_clicked(self, menuitem):
        pass

    def on_generate_physical_model_clicked(self, menuitem):
        pass

    def on_btn_print_clicked(self, menuitem):
        pass

    def on_btn_export_clicked(self, menuitem):
        pass

    def _on_zoomin_clicked(self, menuitem):
        ntbk = self._wTree.get_widget("ntbk_main")

        child = ntbk.get_nth_page(ntbk.get_current_page())

        if child == None:
            log.error("Troubles with the zoomin callback")

        canvas = child.get_data("canvas")

        current_scale = canvas.get_property("scale")
        canvas.set_scale(current_scale + 0.1)

    def on_zoomout_clicked(self, menuitem):
        ntbk = self._wTree.get_widget("ntbk_main")

        child = ntbk.get_nth_page(ntbk.get_current_page())

        if child == None:
            log.error("Troubles with the zoomin callback")

        canvas = child.get_data("canvas")

        current_scale = canvas.get_property("scale")
        if current_scale < 0.1:
            return

        canvas.set_scale(current_scale - 0.1)

    def on_btn_send_to_back_clicked(self, menuitem):
        pass

    def on_btn_send_to_front_clicked(self, menuitem):
        pass

    def on_edit_preferences_clicked(self, menuitem):
        pass

    def on_show_help_clicked(self, menuitem):
        pass

    def on_about_clicked(self, menuitem):
        pass

    def _on_files_list_row_activated(self, treeview, path, view_column):

        ntbk = self._wTree.get_widget("ntbk_main")

        for x in self._files_opened:
            if x[0] == self._files_list[path[0]]:
                log.debug("Trying to open an already opened file")
                page_num = ntbk.page_num(x[1].scrolled_win)
                if page_num == -1:
                    log.debug("The child could not be found inside the main notebook")
                    return
                else:
                    ntbk.set_current_page(page_num)
                    return

        new_canvas = self._control.construct_model(self._files_list[path[0]])

        if new_canvas == None:
            return

        self._files_opened.append((self._files_list[path[0]],new_canvas))

        ## hbox = gtk.HBox()
        ## widget = gtk.Label(os.path.basename(self._files_list[path[0]]))
        ## hbox.pack_start(widget)

        ## button = gtk.Button()
        ## hbox.pack_start(button)
        ## img = gtk.Image()
        ## img.set_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
        ## button.add(img)

        ## button.connect("clicked", self._on_btn_close_model_clicked)
        ## hbox.show_all()
        label = gtk.Label(os.path.basename(self._files_list[path[0]]))
        ntbk.append_page(new_canvas.scrolled_win, label)
        ntbk.set_current_page(-1)

    def _reload_files_list(self):
        "Debe ser llamada cada vez que la lista de archivos cambie (files_list)"
        liststore = gtk.ListStore(gobject.TYPE_STRING)
        treeview = self._wTree.get_widget("files_list")

        treeview.set_model(liststore)

        for elem in self._files_list:
            liststore.append([os.path.basename(str(elem))])

        cols = treeview.get_columns()
        for i in cols:
            treeview.remove_column(i)

        treeviewcol = gtk.TreeViewColumn("Modelos")
        treeview.append_column(treeviewcol)
        cell = gtk.CellRendererText()
        treeviewcol.pack_start(cell)
        treeviewcol.add_attribute(cell, "text", 0)

    def _remove_from_statusbar(self, context_id, msg_id):
        """Remueve el mensaje definido por context_id y msg_id.

        Retorna False para que gobject.timeout_add deje de llamar a la funcion"""
        statusbar = self._wTree.get_widget("statusbar")
        statusbar.remove(context_id, msg_id)

        return False #stop being called by gobject.timeout_add

    def _construct_toolbar(self):
        "Construye la barra de herramientas y el menu usando GtkUIManager"
        log.debug("Constructing the toolbar")

        uifile = resource_filename('rascase.resources.uidefs', 'ui.xml')

        self._uimanager = gtk.UIManager()
        accel_group = self._uimanager.get_accel_group()
        self._window.add_accel_group(accel_group)

        action_group = gtk.ActionGroup('my_actions')
        action_group.add_actions([#TODO:finish actions
            ('File', None, '_Archivo', None, None, None),
            ('NewLogicalModel', gtk.STOCK_NEW, 'Nuevo modelo lógico', '<Control>n', None,
             self._on_new_model),
            ('OpenModel', gtk.STOCK_OPEN, None, '<Control>o', None,
             self.on_open_model),
            ('Save', gtk.STOCK_SAVE, None, '<Control>s', None,
             self._on_save_model),
            ('SaveAs', gtk.STOCK_SAVE_AS, None, None, None,
             self.on_save_model_as),
            ('Print', gtk.STOCK_PRINT, None, '<Control>p', None,
             self.on_btn_print_clicked),
            ('CloseModel', gtk.STOCK_CLOSE, 'Cerrar Modelo', '<Control>w', None,
             self._on_close_file_clicked),
            ('Quit', gtk.STOCK_QUIT, None, '<Control>q', None,
             self._on_quit_selected),
            ('Project', None, '_Proyecto', None, None, None),
            ('NewProject', gtk.STOCK_NEW, None, '', 'Nuevo Proyecto',
             self._on_new_project),
            ('OpenProject', gtk.STOCK_OPEN, None, '', 'Abrir proyecto',
             self._on_open_project),
            ('SaveProject', gtk.STOCK_SAVE, None, '', 'Guardar proyecto',
             self._on_save_project),
            ('AddModel', gtk.STOCK_ADD, None, None, 'Añadir un modelo',
             self.on_add_model_to_project),
            ('RemoveModel', gtk.STOCK_REMOVE, None, None, 'Remover modelo del proyecto',
             self.on_remove_model),
            ('DeleteModel', gtk.STOCK_DELETE, None, None, 'Borrar el modelo',
             self.on_delete_model),
            ('Edit', None, '_Editar', None, None, None),
            ('EditElement', gtk.STOCK_EDIT, None, None, 'Editar el elemento seleccionado',
             self.on_edit_component_clicked),
            ('DeleteElement', gtk.STOCK_DELETE, None, None, 'Borrar el elemento seleccionado',
             self.on_delete_component_clicked),
            ('EditPreferences', gtk.STOCK_PREFERENCES, None, None, 'Editar las preferencias',
             self.on_edit_preferences_clicked),
            ('Help', None, 'A_yuda', None, None, None),
            ('ShowHelp', gtk.STOCK_HELP, None, 'F1', None,
             self.on_show_help_clicked),
            ('About', gtk.STOCK_ABOUT, None, None, None,
             self.on_about_clicked),
            ('Entity', gtk.STOCK_MISSING_IMAGE, 'Entidad', None, None,
             self._on_add_entity_clicked),
            ('Relationship', gtk.STOCK_MISSING_IMAGE, 'Relación', None, None,
             self._on_add_relationship_clicked),
            ('Inheritance', gtk.STOCK_MISSING_IMAGE, 'Herencia', None, None,
             self.on_add_inheritance_clicked),
            ('Label', gtk.STOCK_MISSING_IMAGE, 'Etiqueta', None, None,
             self._on_add_label_clicked),
            ('Rectangle', gtk.STOCK_MISSING_IMAGE, 'Rectangulo', None, None,
             self.on_add_rectangle_clicked),
            ('ZoomIn', gtk.STOCK_ZOOM_IN, None, None, None,
             self._on_zoomin_clicked),
            ('ZoomOut', gtk.STOCK_ZOOM_OUT, None, None, None,
             self.on_zoomout_clicked),
            ('SendToBack', gtk.STOCK_GO_DOWN, 'Enviar atras', None, None,
             self.on_btn_send_to_back_clicked),
            ('SendToFront', gtk.STOCK_GO_UP, 'Enviar al frente', None, None,
             self.on_btn_send_to_front_clicked)])

        self._uimanager.insert_action_group(action_group, 0)
        self._uimanager.add_ui_from_file(uifile)

        box = self._wTree.get_widget("vbox_main")
        #pack the menubar
        menubar = self._uimanager.get_widget("/menubar")
        box.pack_start(menubar, False)
        box.reorder_child(menubar, 0)
        #pack the toolbar
        toolbar = self._uimanager.get_widget("/toolbar")
        box.pack_start(toolbar, False)
        box.reorder_child(toolbar, 1)

    def get_current_path(self):

        ntbk = self._wTree.get_widget("ntbk_main")

        child = ntbk.get_nth_page(ntbk.get_current_page())

        if child == None:
            return None

        canvas = child.get_data("canvas")

        for x in self._files_opened:
            if x[1] == canvas:
                return x[0]

        return None

    def get_canvas_from_path(self, filepath):
        "Retorna el canvas asociado a un archivo"
        for x in self._files_opened:
            if x[0] == filepath:
                return x[1]

        return None

    def get_window(self):
        "retorna la ventana principal, para ser utilizada en los dialogos como ventana padre"
        return self._window

