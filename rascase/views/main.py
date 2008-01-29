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

import logging
import gobject
import gtk
import gtk.glade
import goocanvas

from pkg_resources import resource_filename

from rascase.views import components

class ViewMainWindow:
    """Vista principal

    En esta vista se despliegan los elementos más importantes del software como el canvas, la barra de herramientas y de menu, entre otros

    """
    def __init__(self,control, file_=None):
        logging.getLogger('views.main').info('ViewMainWindow.__init__: file_=%s', file_)
        self.control = control #control que es dueño de la vista
        self.gladefile = resource_filename("rascase.resources.glade", "wndmain.glade")
        self.wTree = gtk.glade.XML(self.gladefile)

        ## widgets
        self._main_toolbar = None
        self._elements_toolbar = None
        self._menubar = None

        ## properties
        self._files_opened = None
        self._files_list = None
        self._canvas_list = None
        self._selected_item = None

        signals_dic = {"on_wndmain_delete_event":gtk.main_quit}
        self.wTree.signal_autoconnect(signals_dic)

        # se ponen los archivos en el files_list
        ## files_list = self.wTree.get_widget("files_list")
        ## files_list_model = gtk.ListStore(gobject.TYPE_STRING)
        ## files_list_model.append(["ejemplo.rxl"])
        ## files_list_model.append(["ejemplo2.rxl"])
        ## files_list_model.append(["webshop.rxl"])
        ## files_list_model.append(["libreria.rxl"])
        ## files_list.set_model(files_list_model)
        ## tvcol = gtk.TreeViewColumn("Modelo")
        ## files_list.append_column(tvcol)
        ## cell = gtk.CellRendererText()
        ## tvcol.pack_start(cell)
        ## tvcol.add_attribute(cell, 'text', 0)


        # the properties of the window were defined
        self._win = self.wTree.get_widget("wndmain")
        self._win.set_default_size(600,500)
        self._win.set_title("RasCASE")
        if self._win is None:
            print "self.win es none"

        self._construct_toolbar()

        self._win.show_all()

    def _construct_toolbar(self):
        uifile = resource_filename('rascase.resources.uidefs', 'ui.xml')

        self._uimanager = gtk.UIManager()
        accel_group = self._uimanager.get_accel_group()
        self._win.add_accel_group(accel_group)

        action_group = gtk.ActionGroup('my_actions')
        action_group.add_actions([#TODO:finish actions
            ('File', None, '_Archivo', None, None, None),
            ('NewLogicalModel', gtk.STOCK_NEW, 'Nuevo modelo lógico', '<Control>n', None,
             self.on_new_model),
            ('OpenModel', gtk.STOCK_OPEN, None, '<Control>o', None,
             self.on_open_model),
            ('Save', gtk.STOCK_SAVE, None, '<Control>s', None,
             self.on_save_model),
            ('SaveAs', gtk.STOCK_SAVE_AS, None, None, None,
             self.on_save_model),
            ('Print', gtk.STOCK_PRINT, None, '<Control>p', None,
             self.on_btn_print_clicked),
            ('CloseModel', gtk.STOCK_CLOSE, 'Cerrar Modelo', '<Control>w', None,
             self.on_close_file_clicked),
            ('Quit', gtk.STOCK_QUIT, None, '<Control>q', None,
             self.on_quit_selected),
            ('Project', None, '_Proyecto', None, None, None),
            ('OpenProject', gtk.STOCK_OPEN, None, '', 'Abrir proyecto',
             self.on_open_project),
            ('AddModel', gtk.STOCK_ADD, None, None, 'Añadir un modelo',
             self.on_add_model_to_project),
            ('RemoveModel', gtk.STOCK_REMOVE, None, None, 'Remover modelo del proyecto',
             self.on_remove_model),
            ('DeleteModel', gtk.STOCK_DELETE, None, None, 'Remover modelo del proyecto y eliminar el modelo',
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
             self.on_add_entity_clicked),
            ('Relationship', gtk.STOCK_MISSING_IMAGE, 'Relación', None, None,
             self.on_add_relationship_clicked),
            ('Inheritance', gtk.STOCK_MISSING_IMAGE, 'Herencia', None, None,
             self.on_add_inheritance_clicked),
            ('Label', gtk.STOCK_MISSING_IMAGE, 'Etiqueta', None, None,
             self.on_add_label_clicked),
            ('Rectangle', gtk.STOCK_MISSING_IMAGE, 'Rectangulo', None, None,
             self.on_add_relationship_clicked),
            ('ZoomIn', gtk.STOCK_ZOOM_IN, None, None, None,
             self.on_zoomin_clicked),
            ('ZoomOut', gtk.STOCK_ZOOM_OUT, None, None, None,
             self.on_zoomout_clicked),
            ('SendToBack', gtk.STOCK_GO_DOWN, 'Enviar atras', None, None,
             self.on_btn_send_to_back_clicked),
            ('SendToFront', gtk.STOCK_GO_UP, 'Enviar al frente', None, None,
             self.on_btn_send_to_front_clicked)])

        self._uimanager.insert_action_group(action_group, 0)
        self._uimanager.add_ui_from_file(uifile)

        box = self.wTree.get_widget("vbox_main")
        #pack the menubar
        menubar = self._uimanager.get_widget("/menubar")
        box.pack_start(menubar, False)
        box.reorder_child(menubar, 0)
        #pack the toolbar
        toolbar = self._uimanager.get_widget("/toolbar")
        box.pack_start(toolbar, False)
        box.reorder_child(toolbar, 1)

    # signals

    def on_quit_selected(self, menuitem):
        pass

    def on_new_project(self, menuitem):
        pass

    def on_new_model(self, menuitem):
        pass

    def on_open_project(self, menuitem):
        pass

    def on_open_model(self, menuitem):
        pass

    def on_save_model(self, menuitem):
        pass

    def on_add_model_to_project(self, menuitem):
        pass

    def on_remove_model(self, menuitem): #remove the model from the project
        pass

    def on_delete_model(self, menuitem):
        pass

    #on the close button of the gtk.Notebook page is clicked
    def on_close_file_clicked(self, menuitem):
        pass

    def on_add_entity_clicked(self, menuitem):
        pass

    def on_add_relationship_clicked(self, menuitem):
        pass

    def on_add_inheritance_clicked(self, menuitem):
        pass

    def on_add_label_clicked(self, menuitem):
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

    def on_zoomin_clicked(self, menuitem):
        pass

    def on_zoomout_clicked(self, menuitem):
        pass

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

