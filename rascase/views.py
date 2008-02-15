# coding=utf-8
##
## base.py
## Login : <freyes@yoda>
## Started on  Tue Jan 22 11:29:49 2008 Felipe Reyes
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

import gobject
import gtk
import gtk.glade
import goocanvas
##logging system
import logging
log = logging.getLogger('views')
##

from pkg_resources import resource_filename

#Tango colors taken from 
#http://tango.freedesktop.org/Tango_Icon_Theme_Guidelines
TANGO_COLOR_BUTTER_LIGHT = int("fce94f",16)
TANGO_COLOR_BUTTER_MID = int("edd400",16)
TANGO_COLOR_BUTTER_DARK = int("c4a000",16)
TANGO_COLOR_ORANGE_LIGHT = int("fcaf3e",16)
TANGO_COLOR_ORANGE_MID = int("f57900",16)
TANGO_COLOR_ORANGE_DARK = int("ce5c00",16)
TANGO_COLOR_CHOCOLATE_LIGHT = int("e9b96e",16)
TANGO_COLOR_CHOCOLATE_MID = int("c17d11",16)
TANGO_COLOR_CHOCOLATE_DARK = int("8f5902",16)
TANGO_COLOR_CHAMELEON_LIGHT = int("8ae234",16)
TANGO_COLOR_CHAMELEON_MID = int("73d216",16)
TANGO_COLOR_CHAMELEON_DARK = int("4e9a06",16)
TANGO_COLOR_SKYBLUE_LIGHT = int("729fcfff",16)
TANGO_COLOR_SKYBLUE_MID = int("3465a4",16)
TANGO_COLOR_SKYBLUE_DARK = int("204a87",16)
TANGO_COLOR_PLUM_LIGHT = int("ad7fa8",16)
TANGO_COLOR_PLUM_MID = int("75507b",16)
TANGO_COLOR_PLUM_DARK = int("5c3566",16)
TANGO_COLOR_SCARLETRED_LIGHT = int("ef2929",16)
TANGO_COLOR_SCARLETRED_MID = int("cc0000",16)
TANGO_COLOR_SCARLETRED_DARK = int("a40000",16)
TANGO_COLOR_ALUMINIUM1_LIGHT = int("eeeeec",16)
TANGO_COLOR_ALUMINIUM1_MID = int("d3d7cf",16)
TANGO_COLOR_ALUMINIUM1_DARK = int("babdb6",16)
TANGO_COLOR_ALUMINIUM2_LIGHT = int("888a85",16)
TANGO_COLOR_ALUMINIUM2_MID = int("555753",16)
TANGO_COLOR_ALUMINIUM2_DARK = int("2e3436",16)
TRANSPARENT_COLOR = int("000000",16)

class RectBaseComponent:
    def __init__(self, bodytype='rect'):
        self._body = None
        self._dragbox = None
        pass

    def set_x(self, x):
        pass

    def get_x(self):
        pass

    def set_y(self, y):
        pass

    def get_y(self):
        pass

    def set_width(self, width):
        pass

    def get_width(self):
        pass

    def set_height(self, height):
        pass

    def get_height(self):
        pass

    def set_linecolor(self, color):
        pass

    def get_linecolor(self):
        pass

    def set_linewidth(self, width):
        pass

    def get_linewidth(self):
        pass

    def set_fillcolor(self, color):
        pass

    def get_fillcolor(self, color):
        pass

    def on_focus_in(self, item, target, event):
        pass

    def on_focus_out(self, item, target, event):
        pass

    def on_button_press(self, item, target, event):
        pass

    def on_button_release(self, item, target, event):
        pass

    def on_enter_notify(self, item, target, event):
        pass

    def on_leave_notifiy(self, item, target, event):
        pass

    def on_motion(self, item, target, event):
        pass


class DragBox(goocanvas.Rect):

    def __init__(self,name,x,y):
        goocanvas.Rect.__init__(self,
            x = x,
            y = y,
            width = 10,
            height = 10,
            line_width = 0.5,
            fill_color = "black",
            visibility = goocanvas.ITEM_HIDDEN)

        self.name = name
        self._dragging = False

        #conexion de senales
        self.connect("button_press_event",self.on_button_press)
        self.connect("button_release_event",self.on_button_release)
        self.connect("motion_notify_event",self.on_motion)
        self.connect("enter_notify_event",self.on_enter_notify)
        self.connect("leave_notify_event",self.on_leave_notify)


    def is_dragging(self):
        if self._dragging == True:
            return True
        else:
            return False

    #senales
    def on_button_press(self,item,target,event):

        self._dragging = True
        fleur = gtk.gdk.Cursor(gtk.gdk.FLEUR)
        canvas = item.get_canvas ()
        canvas.pointer_grab(item,
                            gtk.gdk.POINTER_MOTION_MASK | gtk.gdk.BUTTON_RELEASE_MASK,
                            fleur, event.time)
        self.drag_x = event.x
        self.drag_y = event.y
        return True

    def on_button_release(self,item,target,event):
        self._dragging = False
        canvas = item.get_canvas ()
        canvas.pointer_ungrab(item, event.time)

        return True

    def on_enter_notify(self,item,target,event):
        item.props.fill_color = "yellow"

    def on_leave_notify(self,item,target,event):
        item.props.fill_color = "black"

    def on_motion(self,item,target,event):
        canvas = item.get_canvas ()

        if not (event.state == gtk.gdk.BUTTON1_MASK) and not self._dragging:
            return False

        new_x = event.x
        new_y = event.y
        if item.name == 'N':
            dif = new_y - self.drag_y
            item.translate(0,dif)

            item.get_parent().get_body().props.height = \
                item.get_parent().get_body().props.height - dif

            item.get_parent().get_body().translate(0,dif)

            #make the dragbox follow the corners of the square
            item.get_parent().dragbox['NW'].translate (0,dif)
            item.get_parent().dragbox['NE'].translate (0,dif)
            item.get_parent().dragbox['W'].translate (0,dif/2)
            item.get_parent().dragbox['E'].translate (0,dif/2)

        elif item.name == 'NE':
            dif_x = new_x - self.drag_x
            dif_y = new_y - self.drag_y
            item.translate(dif_x, dif_y)

            item.get_parent().get_body().props.width = \
                item.get_parent().get_body().props.width + dif_x

            item.get_parent().get_body().props.height = \
                item.get_parent().get_body().props.height - dif_y

            item.get_parent().get_body().translate(0, dif_y)

            #make the dragbox follow the corner
            item.get_parent().dragbox['NW'].translate(0, dif_y)
            item.get_parent().dragbox['N'].translate(dif_x/2, dif_y)
            item.get_parent().dragbox['E'].translate(dif_x, dif_y/2)
            item.get_parent().dragbox['SE'].translate(dif_x, 0)

        elif item.name == 'E':
            dif = new_x - self.drag_x
            item.translate(dif,0)

            item.get_parent().get_body().props.width = \
                item.get_parent().get_body().props.width + dif

            #make the dragbox
            item.get_parent().dragbox['NE'].translate (dif, 0)
            item.get_parent().dragbox['SE'].translate (dif, 0)
            item.get_parent().dragbox['N'].translate (dif/2, 0)
            item.get_parent().dragbox['S'].translate (dif/2, 0)

        elif item.name == 'SE':
            dif_x = new_x - self.drag_x
            dif_y = new_y - self.drag_y
            item.translate(dif_x, dif_y)

            item.get_parent().get_body().props.width = \
                item.get_parent().get_body().props.width + dif_x

            item.get_parent().get_body().props.height = \
                item.get_parent().get_body().props.height + dif_y

            #move the dragbox
            item.get_parent().dragbox['N'].translate (dif_x/2, 0)
            item.get_parent().dragbox['NE'].translate (dif_x, 0)
            item.get_parent().dragbox['E'].translate (dif_x, dif_y/2)
            item.get_parent().dragbox['S'].translate (dif_x/2, dif_y)
            item.get_parent().dragbox['SW'].translate (0, dif_y)
            item.get_parent().dragbox['W'].translate (0, dif_y/2)

        elif item.name == 'S':
            dif = new_y - self.drag_y
            item.translate(0,dif)

            item.get_parent().get_body().props.height = \
                item.get_parent().get_body().props.height + dif

            #move the dragbox
            item.get_parent().dragbox['W'].translate (0, dif/2)
            item.get_parent().dragbox['SW'].translate (0, dif)
            item.get_parent().dragbox['SE'].translate (0, dif)
            item.get_parent().dragbox['E'].translate (0, dif/2)

        elif item.name == 'SW':
            dif_x = new_x - self.drag_x
            dif_y = new_y - self.drag_y
            item.translate(dif_x,dif_y)

            item.get_parent().get_body().props.height = \
                item.get_parent().get_body().props.height + dif_y

            item.get_parent().get_body().props.width = \
                item.get_parent().get_body().props.width - dif_x

            item.get_parent().get_body().translate(dif_x,0)

            #move the dragbox
            item.get_parent().dragbox['N'].translate(dif_x/2, 0)
            item.get_parent().dragbox['NW'].translate (dif_x, 0)
            item.get_parent().dragbox['W'].translate (dif_x, dif_y/2)
            item.get_parent().dragbox['S'].translate (dif_x/2, dif_y)
            item.get_parent().dragbox['SE'].translate (0, dif_y)
            item.get_parent().dragbox['E'].translate (0, dif_y/2)

        elif item.name == 'W':
            dif = new_x - self.drag_x
            item.translate(dif, 0)

            item.get_parent().get_body().props.width = \
                item.get_parent().get_body().props.width - dif

            item.get_parent().get_body().translate(dif,0)

            #move the dragbox
            item.get_parent().dragbox['N'].translate (dif/2, 0)
            item.get_parent().dragbox['NW'].translate (dif, 0)
            item.get_parent().dragbox['SW'].translate (dif, 0)
            item.get_parent().dragbox['S'].translate (dif/2, 0)

        elif item.name == 'NW':
            dif_x = new_x - self.drag_x
            dif_y = new_y - self.drag_y
            item.translate(dif_x,dif_y)
            item.get_parent().get_body().props.height = \
                item.get_parent().get_body().props.height - dif_y

            item.get_parent().get_body().props.width = \
                item.get_parent().get_body().props.width - dif_x

            item.get_parent().get_body().translate(dif_x,dif_y)

            #move the dragbox
            item.get_parent().dragbox['E'].translate (0, dif_y/2)
            item.get_parent().dragbox['NE'].translate (0, dif_y)
            item.get_parent().dragbox['N'].translate (dif_x/2, dif_y)
            item.get_parent().dragbox['W'].translate (dif_x, dif_y/2)
            item.get_parent().dragbox['SW'].translate (dif_x, 0)
            item.get_parent().dragbox['S'].translate (dif_x/2, 0)


class RectangleComponent(RectBaseComponent):
    def __init__(self):
        RectBaseComponent.__init__(self)
        self._transparency = 0.0

    def set_transparency(self, opacity):
        pass

class LabelComponent(RectBaseComponent):
    def __init__(self):
        RectBaseComponent

class LineBaseComponent:
    def __init__(self):
        self._line_width = None
        self._line_color = None

    def set_line_width(self, value):
        pass

    def get_line_width(self):
        pass

    def set_line_color(self, value):
        pass

    def get_line_color(self):
        pass

class RectBaseComponent(goocanvas.Group):

    #define a custom signal
    __gsignals__ = {
        'on-movement': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ())
        }

    _ANCHO = 100
    _ALTO = 200
    _ANCHO_LINEA = 1.0
    _COLOR_RELLENO = TANGO_COLOR_SKYBLUE_LIGHT

    def __init__(self, x, y, fill_color, stroke_color, bodytype='rect'):
        goocanvas.Group.__init__(self,can_focus = True)

        if (bodytype == 'table'):
            self._body = goocanvas.Table(width=EntityComponent._ANCHO,
                                         height=EntityComponent._ALTO,
                                         line_width=EntityComponent._ANCHO_LINEA)

        elif (bodytype == 'rect'):
            self._body = goocanvas.Rect(width=EntityComponent._ANCHO,
                                        height=EntityComponent._ALTO,
                                        line_width=EntityComponent._ANCHO_LINEA,
                                        fill_color_rgb=fill_color,
                                        stroke_color=stroke_color)
        else:
            raise RuntimeError

        self.translate(x, y)
        print EntityComponent._COLOR_RELLENO
        self.add_child(self._body)
        self._dragging= False

        self.dragbox = {
            'NW': rascase.views.base.DragBox('NW',-5,-5),
            'N' : rascase.views.base.DragBox('N', self._ANCHO/2-2.5,-5),
            'NE': rascase.views.base.DragBox('NE',self._ANCHO-5,-5),
            'E' : rascase.views.base.DragBox('E', self._ANCHO-5,self._ALTO/2),
            'SE': rascase.views.base.DragBox('SE',self._ANCHO-5,self._ALTO-5),
            'S' : rascase.views.base.DragBox('S', self._ANCHO/2-2.5,self._ALTO-5),
            'SW': rascase.views.base.DragBox('SW',-5, self._ALTO-5),
            'W' : rascase.views.base.DragBox('W', -5,self._ALTO/2)
            }

        for item in self.dragbox.keys():
            self.add_child(self.dragbox[item])

        #signals del foco
        self.connect("focus_in_event", self.on_focus_in)
        self.connect("focus_out_event", self.on_focus_out)
        self.connect("button_press_event", self.on_double_click_press)
        self.connect("button_press_event",self.on_button_press)
        self.connect("button_release_event",self.on_button_release)
        self.connect("motion_notify_event",self.on_motion)
        self.connect("enter_notify_event",self.on_enter_notify)
        self.connect("leave_notify_event",self.on_leave_notify)


    #senales
    def on_double_click_press(self,item,target,event):
        if event.type == gtk.gdk._2BUTTON_PRESS:
            print "*** se hizo doble click", type(target)


    def on_focus_in (self, item, target_item, event):
        for aux in self.dragbox.keys():
            self.dragbox[aux].props.visibility = goocanvas.ITEM_VISIBLE

    def on_focus_out (self, item, target_item, event):
        for aux in self.dragbox.keys():
            self.dragbox[aux].props.visibility = goocanvas.ITEM_HIDDEN

    def on_button_press(self,item,target,event):
        canvas = item.get_canvas()
        canvas.grab_focus(item)

        for aux in self.dragbox.keys():
            if self.dragbox[aux].is_dragging():
                return True

        self._dragging = True
        fleur = gtk.gdk.Cursor(gtk.gdk.FLEUR)
        canvas = item.get_canvas ()
        canvas.pointer_grab(item,
                        gtk.gdk.POINTER_MOTION_MASK | gtk.gdk.BUTTON_RELEASE_MASK,
                        fleur, event.time)
        self.drag_x = event.x
        self.drag_y = event.y
        return True

    def on_button_release(self,item,target,event):
        for aux in self.dragbox.keys():
            if self.dragbox[aux].is_dragging():
                return True

        self._dragging = False
        canvas = item.get_canvas ()
        canvas.pointer_ungrab(item, event.time)
        return True

    def on_enter_notify(self,item,target,event):
        pass

    def on_leave_notify(self,item,target,event):
        pass

    def on_motion(self,item,target,event):
        for aux in self.dragbox.keys():
            if self.dragbox[aux].is_dragging():
                return True

        canvas = item.get_canvas ()

        if not (event.state == gtk.gdk.BUTTON1_MASK) and not self._dragging:
            return False

        new_x = event.x
        new_y = event.y
        item.translate (new_x - self.drag_x, new_y - self.drag_y)
        self.emit('on-movement')


    def set_x(self, x):
        pass

    def get_x(self):
        pass

    def set_y(self, y):
        pass

    def get_y(self):
        pass

    def set_width(self, width):
        pass

    def get_width(self):
        pass

    def set_height(self, height):
        pass

    def get_height(self):
        pass

    def set_linecolor(self, color):
        pass

    def get_linecolor(self):
        pass

    def set_linewidth(self, width):
        pass

    def get_linewidth(self):
        pass

    def set_fillcolor(self, color):
        pass

    def get_fillcolor(self, color):
        pass


class EntityComponent(RectBaseComponent):

    def __init__(self, x, y, stroke_color, fill_color):
        #goocanvas.Group.__init__(self, can_focus = True)
        RectBaseComponent.__init__(self, x, y, stroke_color, fill_color)

    def add_attribute(self,attribute):
        """Agrega un nuevo atributo a la entidad"""

        self._cuerpo.add_child(attribute)
        self._cuerpo.set_child_properties(attribute,
                                          row=self._num_columns,
                                          column=0,
					  x_align=0.0)
        print "numero de columnas", self._num_columns
        self._num_columns += 1
        self.request_update()

    def get_icon_path(cls):

        filename = resource_filename('rascase.resources.pixmaps', 'entity-icon.png')
        return filename

    get_icon_path = staticmethod(get_icon_path) #makes the method static

    #get-set de propiedad
    def get_body(self):
        """Retorna el cuerpo del objeto

        """
        return self._body


class AttributeComponent(goocanvas.Text):
    """Componente gráfico que se pone dentro de una entidad"""
    def __init__(self, name):
        self.default_value = None #
        self.mandatory = False #
        self.primary_key = False #
        self.data_type = None #
        text = name + "\t"
        if self.mandatory:
            text = text + "True"
        else:
            text = text + "False"
        goocanvas.Text.__init__(self, text=text,
				anchor=gtk.ANCHOR_SE,
				can_focus = False)

    def refresh(self):
        pass

    def set_primary_key (self, valor) :
        pass

    def get_primary_key (self) :
        pass

    def set_default_value (self, value) :
        pass

    def get_default_value (self) :
        pass
    def set_data_type (self, datatype) :
        pass

    def get_data_type (self) :
        pass

    def set_mandatory (self, mandatory) :
        pass

    def get_mandatory (self) :
        pass

class RelationshipComponent(LineBaseComponent):
    def __init__(self, entity1, entity2):
        pass

    def set_cardinality(self, type_):
        pass

    def get_cardinality(self):
        pass

    def set_entity1(self, entity):
        pass

    def get_entity1(self):
        pass

    def set_entity2(self, entity):
        pass

    def get_entity2(self):
        pass

    def on_entity_movement(self, item):
        pass

class InheritanceComponent(LineBaseComponent):
    def __init__(self, father, son):
        self._father = father
        self._son = son

    def set_father(self, father):
        pass

    def get_father(self):
        pass

    def set_son(self, son):
        pass

    def get_son(self):
        pass

    def on_entity_movement(self, item):
        pass

class TableComponent(RectBaseComponent):
    def __init__(self):
        RectBaseComponent.__init__(self)


class ReferenceComponent(LineBaseComponent):
    def __init__(self):
        LineBaseComponent.__init__(self)



class Canvas:
    "Esta clase configura el canvas que provee goocanvas"

    def __init__(self):
        self.scrolled_win = gtk.ScrolledWindow()
        self.scrolled_win.set_shadow_type(gtk.SHADOW_IN)
        self.scrolled_win.show()

        self._mycanvas = goocanvas.Canvas()
        self._mycanvas.set_flags(gtk.CAN_FOCUS)
        self._mycanvas.set_size_request(300, 300)
        self._mycanvas.set_bounds(0, 0, 600, 600)
        root = self._mycanvas.get_root_item()
        self._mycanvas.set_root_item(root)
        self._mycanvas.show()

        self.scrolled_win.add(self._mycanvas)


    def add_child(self, child):
        self._mycanvas.get_root_item().add_child(child)


class RectangleComponent(RectBaseComponent):
    def __init__(self):
        RectBaseComponent.__init__(self)
        self._transparency = 0.0

    def set_transparency(self, opacity):
        pass

class LabelComponent(RectBaseComponent):
    def __init__(self, x, y, text):
        RectBaseComponent.__init__(self)
        self.set_x(x)
        self.set_y(y)
        self._text = text

    def set_text(self, text):
        pass

    def get_text(self):
        pass


class ViewEditEntity:
    def __init__(self, entity, control):
        self._window = None
        self._control = control
        self._entity = entity


    #signals
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

    def on_btn_ok_clicked(self, checkbutton):
        pass

    def on_btn_cancel_clicked(self, checkbutton):
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


class ViewMainWindow:
    """Vista principal

    En esta vista se despliegan los elementos más importantes del software como el canvas, la barra de herramientas y de menu, entre otros

    """
    def __init__(self,control, file_=None):
        log.info('ViewMainWindow.__init__: file_=%s', file_)
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

