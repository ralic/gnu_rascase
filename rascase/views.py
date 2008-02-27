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
import cairo
import os
##logging system
import logging
log = logging.getLogger('views')
##

from pkg_resources import resource_filename

#Tango colors taken from
#http://tango.freedesktop.org/Tango_Icon_Theme_Guidelines
TANGO_COLOR_BUTTER_LIGHT = int("fce94fff",16)
TANGO_COLOR_BUTTER_MID = int("edd400ff",16)
TANGO_COLOR_BUTTER_DARK = int("c4a000ff",16)
TANGO_COLOR_ORANGE_LIGHT = int("fcaf3eff",16)
TANGO_COLOR_ORANGE_MID = int("f57900ff",16)
TANGO_COLOR_ORANGE_DARK = int("ce5c00ff",16)
TANGO_COLOR_CHOCOLATE_LIGHT = int("e9b96eff",16)
TANGO_COLOR_CHOCOLATE_MID = int("c17d11ff",16)
TANGO_COLOR_CHOCOLATE_DARK = int("8f5902ff",16)
TANGO_COLOR_CHAMELEON_LIGHT = int("8ae234ff",16)
TANGO_COLOR_CHAMELEON_MID = int("73d216ff",16)
TANGO_COLOR_CHAMELEON_DARK = int("4e9a06ff",16)
TANGO_COLOR_SKYBLUE_LIGHT = int("729fcfff",16)
TANGO_COLOR_SKYBLUE_MID = int("3465a4ff",16)
TANGO_COLOR_SKYBLUE_DARK = int("204a87ff",16)
TANGO_COLOR_PLUM_LIGHT = int("ad7fa8ff",16)
TANGO_COLOR_PLUM_MID = int("75507bff",16)
TANGO_COLOR_PLUM_DARK = int("5c3566ff",16)
TANGO_COLOR_SCARLETRED_LIGHT = int("ef2929ff",16)
TANGO_COLOR_SCARLETRED_MID = int("cc0000ff",16)
TANGO_COLOR_SCARLETRED_DARK = int("a40000ff",16)
TANGO_COLOR_ALUMINIUM1_LIGHT = int("eeeeecff",16)
TANGO_COLOR_ALUMINIUM1_MID = int("d3d7cfff",16)
TANGO_COLOR_ALUMINIUM1_DARK = int("babdb6ff",16)
TANGO_COLOR_ALUMINIUM2_LIGHT = int("888a85ff",16)
TANGO_COLOR_ALUMINIUM2_MID = int("555753ff",16)
TANGO_COLOR_ALUMINIUM2_DARK = int("2e3436ff",16)
TRANSPARENT_COLOR = int("000000",16)

class RectBaseComponent(goocanvas.Group):
    __gsignals__ = {
        'on-movement': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ())
        }

    #some constants that probably must be deleted :P
    _ANCHO = 100
    _ALTO = 200
    _ANCHO_LINEA = 1.0
    _COLOR_RELLENO = TANGO_COLOR_SKYBLUE_LIGHT

    def __init__(self):
        goocanvas.Group.__init__(self,can_focus = True)

        self._dragbox = None

        self._body = goocanvas.Rect(parent=self,
                                    width=RectBaseComponent._ANCHO,
                                    height=RectBaseComponent._ALTO,
                                    line_width=RectBaseComponent._ANCHO_LINEA,
                                    fill_color_rgba=TANGO_COLOR_SKYBLUE_LIGHT,
                                    stroke_color="black",
                                    antialias=cairo.ANTIALIAS_SUBPIXEL)

        self._x = 0
        self._y = 0
        self.translate(self._x, self._y)

        self._dragging= False
        self.dragbox = {
            'NW': DragBox('NW',-5,-5),
            'N' : DragBox('N', self._ANCHO/2-2.5,-5),
            'NE': DragBox('NE',self._ANCHO-5,-5),
            'E' : DragBox('E', self._ANCHO-5,self._ALTO/2-2.5),
            'SE': DragBox('SE',self._ANCHO-5,self._ALTO-5),
            'S' : DragBox('S', self._ANCHO/2-2.5,self._ALTO-5),
            'SW': DragBox('SW',-5, self._ALTO-5),
            'W' : DragBox('W', -5,self._ALTO/2-2.5)
            }

        for item in self.dragbox.keys():
            self.add_child(self.dragbox[item])

        #signals del foco
        self.connect("focus_in_event", self._on_focus_in)
        self.connect("focus_out_event", self._on_focus_out)
        self.connect("button_press_event", self._on_double_click_press)
        self.connect("button_press_event",self._on_button_press)
        self.connect("button_release_event",self._on_button_release)
        self.connect("motion_notify_event",self._on_motion)

    def set_x(self, x):
        self.translate(x-self._x,0)

    def get_x(self):
        return self._x

    def set_y(self, y):
        self.translate(0, y-self._y)

    def get_y(self):
        return self._y

    def translate(self, diff_x, diff_y):
        goocanvas.Group.translate(self, diff_x, diff_y)
        self._x += diff_x
        self._y += diff_y

    def set_width(self, width):
        self.set_property("width", width)

    def get_width(self):
        return self._body.get_property("width")

    def set_height(self, height):
        self.set_property("height", height)

    def get_height(self):
        return self._body.get_property("height")

    def set_linecolor(self, color):

        self._linecolor = color

        if isinstance(color, str):
            self._body.set_property("stroke-color", color)
        elif isinstance(color, int):
            self._body.set_property("stroke-color-rgba", color)
        else:
            log.debug("passing %s to set_linecolor", color)

    def get_linecolor(self):
        return self._linecolor

    def set_linewidth(self, width):
        self._body.set_property("line-width", width)

    def get_linewidth(self):
        return self._body.get_property("line-width")

    def set_fillcolor(self, color):

        self._fillcolor = color

        if isinstance(color, str):
            self._body.set_property("fill-color", color)
        elif isinstance(color, int) or isinstance(color, long):
            self._body.set_property("fill-color-rgba", color)
        else:
            log.debug("passing %s to set_linecolor", color)

    def get_fillcolor(self):
        return self._fillcolor

    def get_body(self):
        return self._body

    def get_bg(self):
        if hasattr(self, "_bg"):
            return self._bg
        else:
            return None

    #senales
    def _on_double_click_press(self,item,target,event):
        if event.type == gtk.gdk._2BUTTON_PRESS:
            print "*** se hizo doble click", type(target)


    def _on_focus_in (self, item, target_item, event):
        for aux in self.dragbox.keys():
            self.dragbox[aux].props.visibility = goocanvas.ITEM_VISIBLE

    def _on_focus_out (self, item, target_item, event):
        for aux in self.dragbox.keys():
            self.dragbox[aux].props.visibility = goocanvas.ITEM_HIDDEN

    def _on_button_press(self,item,target,event):
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

    def _on_button_release(self,item,target,event):
        for aux in self.dragbox.keys():
            if self.dragbox[aux].is_dragging():
                return True

        self._dragging = False
        canvas = item.get_canvas ()
        canvas.pointer_ungrab(item, event.time)
        return True

    def _on_motion(self,item,target,event):
        for aux in self.dragbox.keys():
            if self.dragbox[aux].is_dragging():
                return True

        canvas = item.get_canvas ()

        if not (event.state == gtk.gdk.BUTTON1_MASK) and not self._dragging:
            return False

        new_x = event.x
        new_y = event.y
        item.translate (new_x - self.drag_x, new_y - self.drag_y)
        self.emit("on-movement")

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
        self.connect("button_press_event",self._on_button_press)
        self.connect("button_release_event",self._on_button_release)
        self.connect("motion_notify_event",self._on_motion)
        self.connect("enter_notify_event",self._on_enter_notify)
        self.connect("leave_notify_event",self._on_leave_notify)


    def is_dragging(self):
        return self._dragging

    #senales
    def _on_button_press(self,item,target,event):

        self._dragging = True
        fleur = gtk.gdk.Cursor(gtk.gdk.FLEUR)
        canvas = item.get_canvas ()
        canvas.pointer_grab(item,
                            gtk.gdk.POINTER_MOTION_MASK | gtk.gdk.BUTTON_RELEASE_MASK,
                            fleur, event.time)
        self.drag_x = event.x
        self.drag_y = event.y
        return True

    def _on_button_release(self,item,target,event):
        self._dragging = False
        canvas = item.get_canvas ()
        canvas.pointer_ungrab(item, event.time)

        return True

    def _on_enter_notify(self,item,target,event):
        item.set_property("fill-color-rgba", TANGO_COLOR_BUTTER_LIGHT)

    def _on_leave_notify(self,item,target,event):
        item.set_property("fill-color-rgba", int("000000ff",16))

    def _on_motion(self,item,target,event):
        canvas = item.get_canvas ()

        if not (event.state == gtk.gdk.BUTTON1_MASK) and not self._dragging:
            return False

        new_x = event.x
        new_y = event.y

        body = item.get_parent().get_body()
        bg = item.get_parent().get_bg()

        if item.name == 'N':
            dif = new_y - self.drag_y
            item.translate(0,dif)

            body.props.height = body.props.height - dif
            body.translate(0,dif)

            # this is trick to get a color behind a goocanvas.Table
            if bg != None:
                bg.props.height = bg.props.height - dif
                bg.translate(0,dif)

            #make the dragbox follow the corners of the square
            item.get_parent().dragbox['NW'].translate (0,dif)
            item.get_parent().dragbox['NE'].translate (0,dif)
            item.get_parent().dragbox['W'].translate (0,dif/2)
            item.get_parent().dragbox['E'].translate (0,dif/2)

        elif item.name == 'NE':
            dif_x = new_x - self.drag_x
            dif_y = new_y - self.drag_y
            item.translate(dif_x, dif_y)

            body.props.width = body.props.width + dif_x
            body.props.height = body.props.height - dif_y
            body.translate(0, dif_y)

            if bg != None:
                bg.props.width = bg.props.width + dif_x
                bg.props.height = bg.props.height - dif_y
                bg.translate(0, dif_y)

            #make the dragbox follow the corner
            item.get_parent().dragbox['NW'].translate(0, dif_y)
            item.get_parent().dragbox['N'].translate(dif_x/2, dif_y)
            item.get_parent().dragbox['E'].translate(dif_x, dif_y/2)
            item.get_parent().dragbox['SE'].translate(dif_x, 0)

        elif item.name == 'E':
            dif = new_x - self.drag_x
            item.translate(dif,0)

            body.props.width = body.props.width + dif

            if bg != None:
                bg.props.width = body.props.width + dif

            #make the dragbox
            item.get_parent().dragbox['NE'].translate (dif, 0)
            item.get_parent().dragbox['SE'].translate (dif, 0)
            item.get_parent().dragbox['N'].translate (dif/2, 0)
            item.get_parent().dragbox['S'].translate (dif/2, 0)

        elif item.name == 'SE':
            dif_x = new_x - self.drag_x
            dif_y = new_y - self.drag_y
            item.translate(dif_x, dif_y)

            body.props.width = body.props.width + dif_x
            body.props.height = body.props.height + dif_y

            if bg != None:
                bg.props.width = bg.props.width + dif_x
                bg.props.height = bg.props.height + dif_y

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

            body.props.height = body.props.height + dif

            if bg != None:
                bg.props.height = bg.props.height + dif

            #move the dragbox
            item.get_parent().dragbox['W'].translate (0, dif/2)
            item.get_parent().dragbox['SW'].translate (0, dif)
            item.get_parent().dragbox['SE'].translate (0, dif)
            item.get_parent().dragbox['E'].translate (0, dif/2)

        elif item.name == 'SW':
            dif_x = new_x - self.drag_x
            dif_y = new_y - self.drag_y
            item.translate(dif_x,dif_y)

            body.props.height = body.props.height + dif_y
            body.props.width = body.props.width - dif_x
            body.translate(dif_x,0)

            if bg != None:
                bg.props.height = bg.props.height + dif_y
                bg.props.width = bg.props.width - dif_x
                bg.translate(dif_x, 0)

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

            body.props.width = body.props.width - dif
            body.translate(dif,0)

            if bg != None:
                bg.props.width = bg.props.width - dif
                bg.translate(dif, 0)

            #move the dragbox
            item.get_parent().dragbox['N'].translate (dif/2, 0)
            item.get_parent().dragbox['NW'].translate (dif, 0)
            item.get_parent().dragbox['SW'].translate (dif, 0)
            item.get_parent().dragbox['S'].translate (dif/2, 0)

        elif item.name == 'NW':
            dif_x = new_x - self.drag_x
            dif_y = new_y - self.drag_y
            item.translate(dif_x,dif_y)

            body.props.height = body.props.height - dif_y
            body.props.width = body.props.width - dif_x
            body.translate(dif_x,dif_y)

            if bg != None:
                bg.props.height = bg.props.height - dif_y
                bg.props.width = bg.props.width - dif_x
                bg.translate(dif_x,dif_y)

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
        self.set_fillcolor(TRANSPARENT_COLOR)
        print self.get_fillcolor()

    def set_transparency(self, opacity):
        pass

class LabelComponent(RectBaseComponent):
    def __init__(self):
        RectBaseComponent.__init__(self)
        # set the default color of the labels
        # TODO: use gconf to let the preferences selected by the user modify this
        self.set_fillcolor(TANGO_COLOR_BUTTER_LIGHT)

        self._bg = goocanvas.Text(parent=self,
                                    text="<b>Etiqueta</b>",
                                    use_markup=True,
                                    font="DejaVu Sans normal 8") #the font need to be parametrized with gconf

    def set_text(self, text):
        self._bg.set_property("text", text)

    def get_text(self):
        return self._bg.get_property("text")

    def _on_focus_in(self, item, target_item, event):
        RectBaseComponent._on_focus_in(self, item, target_item, event)
        print "foco in"

    def set_font(self, font):
        """Define la fuente que debe usar la instancia de LabelComponent

        El parametro font es un string con el mismo formato que el constructor de pango.FontDescription"""
        return self._bg.set_property("font", font)

    def get_font(self):
        "Retorna la fuente que esta usando la instancia de LabelComponent"
        return self._bg.get_property("font")

class EntityComponent(RectBaseComponent):

    def __init__(self, name, x=0, y=0):
        RectBaseComponent.__init__(self)
        self._num_rows = 0
        self._bg = self._body

        self.set_x(x)
        self.set_y(y)

        # this table is the top level table of the EntityComponent
        # only contains the entity name, line separator, attributes table
        self._toptable = goocanvas.Table(parent=self,
                                         width=RectBaseComponent._ANCHO,
                                         height=RectBaseComponent._ALTO,
                                         column_spacing=5,
                                         row_spacing=2,
                                         fill_color="black")

        # the title of the entity
        self._entity_title = goocanvas.Text(text="<b>" + str(name) + "</b>",
                                            use_markup=True,
                                            font="sans 8")

        self._toptable.add_child(self._entity_title)
        self._toptable.set_child_properties(self._entity_title,
                                            row=0,
                                            column=0,
                                            x_align=0.5,
                                            top_padding=5,
                                            left_padding=5)

        #line to use like separator between the entity name and the attributes
        pts = goocanvas.Points([(1,1),(100,1)])
        self._line = goocanvas.Polyline(parent=self._toptable,
                                        points=pts,
                                        stroke_color="black",
                                        line_width=1)

        self._toptable.set_child_properties(self._line,
                                            row=1,
                                            column=0)

        # this table must contain the attributes
        self._body = goocanvas.Table(width=RectBaseComponent._ANCHO,
                                     height=RectBaseComponent._ALTO,
                                     column_spacing=5,
                                     row_spacing=2,
                                     fill_color="black")

        self._toptable.add_child(self._body)
        self._toptable.set_child_properties(self._body,
                                            row=2,
                                            column=0,
                                            x_align=0.0,
                                            top_padding=5)

    def add_attribute(self,attribute):
        """Agrega un nuevo atributo a la entidad"""

        self._body.add_child(attribute.items['name'])
        self._body.set_child_properties(attribute.items['name'],
                                        row=self._num_rows,
                                        column=0,
                                        x_align=0.0,
                                        left_padding=5)

        self._body.add_child(attribute.items['mandatory'])
        self._body.set_child_properties(attribute.items['mandatory'],
                                        row=self._num_rows,
                                        column=1,
                                        x_align=0.5)

        self._body.add_child(attribute.items['datatype'])
        self._body.set_child_properties(attribute.items['datatype'],
                                        row=self._num_rows,
                                        column=2,
                                        x_align=0.0)

        self._num_rows += 1
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
    def __init__(self, name, datatype, default_value=None, pk=False, mandatory=False):

        self._name = name
        self._default_value = default_value
        self._mandatory = mandatory
        self._primary_key = pk
        self._data_type = datatype[0]
        if len(datatype) > 1:
            self._data_type_length = datatype[1]
        else:
            self._data_type_length = None

        ## goocanvas.Text.__init__(self, text=self._build_text(),
        ##                         use_markup=True,
	## 			anchor=gtk.ANCHOR_SE,
	## 			can_focus = False,
        ##                         font="mono 8")
        if self._mandatory:
            text_m = "[M]"
        else:
            text_m = ""

        if self._primary_key:
            text_name = "<u>" + self._name + "</u>"
        else:
            text_name = self._name

        #FIXME: this should not happen, the controller must do this
        from rascase.core import LogicalDataType
        text_dt = LogicalDataType.to_string(self._data_type)
        if isinstance(self._data_type_length, int):
            text_dt = text_dt + "(" + str(self._data_type_length) + ")"

        self.items = {'mandatory':goocanvas.Text(text=text_m, use_markup=True, font="sans 8"),
                      'name':goocanvas.Text(text=text_name, use_markup=True, font="sans 8"),
                      'datatype':goocanvas.Text(text=text_dt, use_markup=True, font="sans 8")
                      }

    def refresh(self):
        if self._mandatory:
            text_m = "[M]"
        else:
            text_m = ""

        if self._primary_key:
            text_name = "<u>" + self._name + "</u>"
        else:
            text_name = self._name

        #FIXME: this should not happen, the controller must do this
        from rascase.core import LogicalDataType
        text_dt = LogicalDataType.to_string(self._data_type)
        if isinstance(self._data_type_length, int):
            text_dt = text_dt + "(" + str(self._data_type_length) + ")"

        self.items['mandatory'].set_property("text", text_m)
        self.items['name'].set_property("text", text_name)
        self.items['datatype'].set_property("text", text_dt)

    def set_primary_key (self, valor) :
        self._primary_key = valor

    def get_primary_key (self) :
        return self._primary_key

    def set_default_value (self, value) :
        self._default_value = value

    def get_default_value (self) :
        return self._default_value

    def set_data_type (self, datatype):
        """Define el tipo de dato del atributo, datatype es una tuple() de uno o dos elementos,
        el primer elemento es el tipo de dato y el segundo elemento (opcional) es un entero
        que representa el largo del tipo de dato.

        Por ejemplo datatype=(LogicalDataType.VARCHAR, 10) representa un varchar de largo 10
        """
        self._data_type = datatype[0]

        if len(datatype) > 1:
            self._data_type_length = datatype[1]
        else:
            self._data_type_length = None

    def get_data_type (self) :
        if self._data_type_length != None:
            return (self._data_type, self._data_type_length)
        else:
            return (self._data_type,)

    def set_mandatory (self, mandatory) :
        self._mandatory = mandatory

    def get_mandatory (self) :
        return self._mandatory


class LineBaseComponent(goocanvas.Polyline):
    def __init__(self, **kargs):
        goocanvas.Polyline.__init__(self, **kargs)

        if "line_width" in kargs.keys():
            self._line_width = kargs["line_width"]
        else:
            self._line_width = None

        if "line_color" in kargs.keys():
            self._line_color = kargs["line_color"]
        else:
            self._line_color = int("000000",16)

    def set_linewidth(self, value):
        self.set_property("line-width", value)
        self._line_width = value

    def get_linewidth(self):
        return self._line_width

    def set_linecolor(self, value):

        if isinstance(value,str):
            self.set_property("stroke-color", value)
        else:
            self.set_property("stroke-color-rgba", value)

        self._line_color = value

    def get_linecolor(self):
        return self._line_color

class RelationshipComponent(LineBaseComponent):
    def __init__(self, entity1, entity2, cardinality, dependent):

        self._cardinality = cardinality
        self._dependent = dependent
        self._entity1 = entity1
        self._entity2 = entity2

        self._entity1.connect("on-movement",self._on_entity_movement)
        self._entity2.connect("on-movement",self._on_entity_movement)

        LineBaseComponent.__init__(self,points=self._build_points(),
                                   stroke_color="black")


    def _build_points(self):

        points_list = list()

        if self._entity1.get_x() < self._entity2.get_x():
            x1 = self._entity1.get_x() + self._entity1.get_width()
            x2 = self._entity2.get_x()
        else:
            x1 = self._entity1.get_x()# - self._entity1.get_width()
            x2 = self._entity2.get_x() + self._entity2.get_width()

        y1 = self._entity1.get_y() + self._entity1.get_height()/2
        y2 = self._entity2.get_y() + self._entity2.get_height()/2

        points_list.append((x1,y1))

        from rascase.core import Relationship

        # TODO: hacer que las lineas varien segun la configuracion de la relacion
        #if self.cardinality == Relationship.CARDINALITY_

        if self._entity1.get_x() < self._entity2.get_x():
            p1 = (x2-25, y2)
            points_list.append(p1)

            p2 = (p1[0] + 5, p1[1])
            points_list.append(p2)

            p3 = (p2[0] + 10, p2[1] - 10)
            points_list.append(p3)

            p4 = (p3[0], p3[1] + 20)
            points_list.append(p4)

            p5 = (p2[0], p2[1])
            points_list.append(p5)
        else:
            p1 = (x2+25, y2)
            points_list.append(p1)

            p2 = (p1[0] - 5, p1[1])
            points_list.append(p2)

            p3 = (p2[0] - 10, p2[1] - 10)
            points_list.append(p3)

            p4 = (p3[0], p3[1] + 20)
            points_list.append(p4)

            p5 = (p2[0], p2[1])
            points_list.append(p5)

        points_list.append((x2,y2))
        ## p2_x = p1_x + 10
        ## p2_y = (y2-y1-x2+x1)/(y2-y1+x2-x1)*(p2_x-p1_x)+p1_y

        pts = goocanvas.Points(points_list)

        return pts

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

    def _on_entity_movement(self, item):
        self.set_property("points", self._build_points())

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

#physical model components

class TableComponent(RectBaseComponent):
    def __init__(self):
        RectBaseComponent.__init__(self)


class ReferenceComponent(LineBaseComponent):
    def __init__(self):
        LineBaseComponent.__init__(self)



class Canvas(goocanvas.Canvas):
    "Esta clase configura el canvas que provee goocanvas"

    def __init__(self, **kargs):
        goocanvas.Canvas.__init__(self, **kargs)
        self.scrolled_win = gtk.ScrolledWindow()
        self.scrolled_win.set_shadow_type(gtk.SHADOW_IN)
        self.scrolled_win.show()

        self.set_flags(gtk.CAN_FOCUS)
        self.set_size_request(300, 300)
        self.set_bounds(0, 0, 600, 600)
        root = self.get_root_item()
        self.set_root_item(root)
        self.show()

        self.scrolled_win.add(self)

    def add_child(self, item):
        self.get_root_item().add_child(item)

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


class ViewMainWindow:
    """Vista principal

    En esta vista se despliegan los elementos más importantes del software como el canvas, la barra de herramientas y de menu, entre otros

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
        self._files_opened = None
        self._files_list = None
        self._canvas_list = None
        self._selected_item = None


        # the association of the signals defined inside glade and the python methods
        signals_dic = {"on_wndmain_delete_event":self._on_delete_main_window,
                       "on_files_list_row_activated":self._on_files_list_row_activated}
        self._wTree.signal_autoconnect(signals_dic)

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
        self._window = self._wTree.get_widget("wndmain")
        self._window.set_default_size(600,500)
        self._window.set_title("RasCASE")
        if self._window is None:
            print "self.win es none"

        self._construct_toolbar()

        self._window.show_all()

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
             self._on_quit_selected),
            ('Project', None, '_Proyecto', None, None, None),
            ('OpenProject', gtk.STOCK_OPEN, None, '', 'Abrir proyecto',
             self._on_open_project),
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

        box = self._wTree.get_widget("vbox_main")
        #pack the menubar
        menubar = self._uimanager.get_widget("/menubar")
        box.pack_start(menubar, False)
        box.reorder_child(menubar, 0)
        #pack the toolbar
        toolbar = self._uimanager.get_widget("/toolbar")
        box.pack_start(toolbar, False)
        box.reorder_child(toolbar, 1)

    # signals

    def _on_delete_main_window(self, widget, event):
        "callback conectado al evento 'delete' de la ventana principal"

        widget = self._uimanager.get_widget("/menubar/File/Quit")

        widget.activate()
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

    def on_new_project(self, menuitem):
        pass

    def on_new_model(self, menuitem):
        pass

    def _on_open_project(self, menuitem):

        # obtain the list of models associated to the project
        self._files_list = self._control.open_project(path=None)

        liststore = gtk.ListStore(gobject.TYPE_STRING)
        treeview = self._wTree.get_widget("files_list")

        treeview.set_model(liststore)

        for elem in self._files_list:
            liststore.append([os.path.basename(str(elem))])

        treeviewcol = gtk.TreeViewColumn("Modelos")
        treeview.append_column(treeviewcol)
        cell = gtk.CellRendererText()
        treeviewcol.pack_start(cell)
        treeviewcol.add_attribute(cell, "text", 0)

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

    def _on_files_list_row_activated(self, treeview, path, view_column):
        canvas = self._control.construct_model(self._files_list[path[0]])
        pass

    def get_window(self):
        "retorna la ventana principal, para ser utilizada en los dialogos como ventana padre"
        return self._window

