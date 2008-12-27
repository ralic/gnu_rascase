# coding=utf-8
##
## items.py
## Login : <freyes@yoda.starwars.cl>
## Started on  Sat Dec 27 13:33:29 2008 Felipe Reyes
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
import goocanvas
import cairo
import pangocairo
import pango
import os
import math
from color import *
##logging system
import logging
log = logging.getLogger('items')
##


class RectBaseComponent(goocanvas.ItemSimple, goocanvas.Item):
    __gsignals__ = {
        'on-movement': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ()),
        'on-double-click': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ()),
        'changed-dimensions': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ())
        }

    def __init__(self, **kwargs):


        ### properties
        if 'width' in kwargs:
            self.width = kwargs['width']
            del kwargs['width']
        else:
            self.width = 100

        if 'height' in kwargs:
            self.height = kwargs['height']
            del kwargs['height']
        else:
            self.height = 200

        if 'x' in kwargs:
            self._x = kwargs['x']
            del kwargs['x']
        else:
            self._x = 0

        if 'y' in kwargs:
            self._y = kwargs['y']
            del kwargs['y']
        else:
            self._y = 0

        goocanvas.ItemSimple.__init__(self, **kwargs)

        self.translate(self.x, self.y)
        self.line_width = self.get_property("line-width")
        self._dragging= False

        #signals del foco
        self.connect("focus_in_event", self._on_focus_in)
        self.connect("focus_out_event", self._on_focus_out)
        self.connect("button_press_event", self._on_double_click_press)
        self.connect("button_press_event",self._on_button_press)
        self.connect("button_release_event",self._on_button_release)
        self.connect("motion_notify_event",self._on_motion)

    def set_x(self, x):
        self.translate(float(x)-self._x,0)
        self._x = x

    def get_x(self):
        return self._x

    def set_y(self, y):
        self.translate(0, y-self._y)
        self._y = y

    def get_y(self):
        return self._y

    def translate(self, diff_x, diff_y):
        goocanvas.ItemSimple.translate(self, diff_x, diff_y)
        self._x += diff_x
        self._y += diff_y

    def set_width(self, width):
        assert width is not None

        self._width = float(width)

    def get_width(self):
        return self._width

    def set_height(self, height):
        assert height is not None

        self._height = float(height)

    def get_height(self):
        return self._height

    def set_linecolor(self, color):

        if isinstance(color, str) or isinstance(color, unicode):
            self.set_property("stroke-color", color)
        elif isinstance(color, int) or isinstance(color, long):
            self.set_property("stroke-color-rgba", color)
        else:
            log.error("passing %s to set_linecolor (%s)", color, type(color))

        self._linecolor = self.get_property("stroke-color-rgba")

    def get_linecolor(self):
        return self.get_property("stroke-color-rgba")

    def set_linewidth(self, width):
        self.set_property("line-width", width)

    def get_linewidth(self):
        return self.get_property("line-width")

    def set_fillcolor(self, color):

        self._fillcolor = color

        if isinstance(color, str):
            self.set_property("fill-color", color)
        elif isinstance(color, int) or isinstance(color, long):
            self.set_property("fill-color-rgba", color)
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
            self.emit("on-double-click")

    def _on_focus_in (self, item, target_item, event):
        if hasattr(self, "_old_linecolor"):
            return

        self._old_linecolor = self.get_linecolor()
        self.set_linecolor(0x000000FF)

    def _on_focus_out (self, item, target_item, event):
        self.set_linecolor(self._old_linecolor)
        del self._old_linecolor

    def _on_button_press(self,item,target,event):
        canvas = item.get_canvas()
        canvas.grab_focus(item)

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

    def _on_motion(self,item,target,event):

        if not (event.state == gtk.gdk.BUTTON1_MASK) and not self._dragging:
            return False

        new_x = event.x
        new_y = event.y
        item.translate (new_x - self.drag_x, new_y - self.drag_y)
        self.emit("on-movement")

    ### item implementation

    def do_simple_create_path(self, cr):
        cr.rectangle(0, 0, self.width, self.height)

    x = property(get_x, set_x, None, "The x coordinate of the item")
    y = property(get_y, set_y, None, "The y coordinate of the item")
    width = property(get_width, set_width, None, "The width of the item")
    height = property(get_height, set_height, None, "The height of the item")

gobject.type_register(RectBaseComponent)

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
                if isinstance(bg, goocanvas.Text):
                    pass
                else:
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
                if isinstance(bg, goocanvas.Text):
                    pass
                else:
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
                if isinstance(bg, goocanvas.Text):
                    pass
                else:
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
                if isinstance(bg, goocanvas.Text):
                    pass
                else:
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
                if isinstance(bg, goocanvas.Text):
                    pass
                else:
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
                if isinstance(bg, goocanvas.Text):
                    pass
                else:
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

        item.get_parent().emit("changed-dimensions")


class RectangleComponent(RectBaseComponent):
    def __init__(self, **kwargs):
        RectBaseComponent.__init__(self, **kwargs)
        self._transparency = 0.0
        self.set_fillcolor(TRANSPARENT_COLOR)

    def set_transparency(self, opacity):
        pass

gobject.type_register(RectangleComponent)

class LabelComponent(RectBaseComponent):

    def __init__(self, control, **kwargs):

        ### setup properties

        #text
        if 'text' in kwargs:
            self.text = unicode(kwargs['text'])
            del kwargs['text']
        else:
            self.text = "Label"

        #use_markup
        if 'use_markup' in kwargs:
            self.use_markup = unicode(kwargs['use_markup'])
            del kwargs['use_markup']
        else:
            self.use_markup = False

        #font
        if 'font' in kwargs:
            self.font = unicode(kwargs['font'])
            del kwargs['font']
        else:
            self.font = 'Sans'

        #font_size
        if 'font_size' in kwargs:
            self.font_size = float(kwargs['font_size'])
            del kwargs['font_size']
        else:
            self.font_size = 10.0

        #text_color
        if 'text_color' in kwargs:
            self.text_color = gtk.gdk.color_parse(kwargs['text_color'])
            del kwargs['text_color']
        else:
            self.text_color = gtk.gdk.Color(0, 0, 1)


        RectBaseComponent.__init__(self, **kwargs)
        self._control = control

        self.connect("on-double-click", self._on_edit_label_selected)

    def set_text(self, text):
        self._bg.set_property("text", text)
        self.translate(0,0)

    def get_text(self):
        return self._bg.get_property("text")

    def set_font(self, font):
        """Define la fuente que debe usar la instancia de LabelComponent

        El parametro font es un string con el mismo formato que el constructor de pango.FontDescription"""
        self._bg.set_property("font", font)
        self.translate(0,0)

    def get_font(self):
        "Retorna la fuente que esta usando la instancia de LabelComponent"
        return self._bg.get_property("font")

    #signals
    def _on_edit_label_selected(self, item):
        #self._control.
        pass

    ### item implementation
    def do_simple_paint(self, cr, bounds):
        cr.move_to(10,20)
        pangocr = pangocairo.CairoContext(cr)
        layout = pangocr.create_layout()

        if self.use_markup:
            layout.set_markup(self.text)
        else:
            layout.set_text(self.text)

        layout.set_wrap(pango.WRAP_WORD)
        layout.set_width(int(self.width*pango.SCALE))
        needed_height = layout.get_size()[1]/pango.SCALE
        if self.height < needed_height:
            self.height = needed_height

        self.bounds.x1 = float(self.x)
        self.bounds.y1 = float(self.y)
        self.bounds.x2 = float(self.width) +200
        self.bounds.y2 = float(self.height)+200

        RectBaseComponent.do_simple_paint(self, cr, bounds)

        desc = pango.FontDescription("%s %s" % (self.font, str(self.font_size)))
        layout.set_font_description(desc)
        cr.set_source_rgb (gdk2rgb(self.text_color)[0],
                           gdk2rgb(self.text_color)[1],
                           gdk2rgb(self.text_color)[2])
        #pangocairo.CairoContext.update_layout(layout)
        pangocr.update_layout(layout)
        #pangocairo.CairoContext.show_layout(layout)
        pangocr.show_layout(layout)
        pangocr.layout_path(layout)
        ## cr.move_to(self.line_width + 5, self.line_width + 10)

        ## cr.set_source_rgb (gdk2rgb(self.text_color)[0],
        ##                    gdk2rgb(self.text_color)[1],
        ##                    gdk2rgb(self.text_color)[2])

        ## cr.select_font_face(self.font,
        ##                     cairo.FONT_SLANT_NORMAL,
        ##                     cairo.FONT_WEIGHT_BOLD)

        ## cr.set_font_size(self.font_size)
        ## cr.show_text (self.text)


    def do_simple_update (self, cr):

        RectBaseComponent.do_simple_update(self, cr)
        half_lw = self.line_width/2
        self.bounds.x1 = float(self.x - half_lw)
        self.bounds.y1 = float(self.y - half_lw)
        self.bounds.x2 = float(self.x + self.width + half_lw)
        self.bounds.y2 = float(self.y + self.height + half_lw)
        return None

gobject.type_register(LabelComponent)


class EntityComponent(RectBaseComponent):

    def __init__(self, name, x=0, y=0, width=100, height=100):
        RectBaseComponent.__init__(self, width=width, height=height)
        self.attr_list = list()
        self._num_rows = 0
        self._bg = self._body

        self.set_x(float(x))
        self.set_y(float(y))

        # this table is the top level table of the EntityComponent
        # only contains the entity name, line separator, attributes table
        self._toptable = goocanvas.Table(parent=self,
                                         width=self.get_width(),
                                         height=self.get_height(),
                                         column_spacing=5,
                                         row_spacing=2,
                                         fill_color="black")

        # the title of the entity
        self._name = name
        self._entity_title = goocanvas.Text(text="<b>" + str(self._name) + "</b>",
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
        self._body = goocanvas.Table(width=self.get_width(),
                                     height=self.get_height(),
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
        "Agrega un nuevo atributo a la entidad"

        self.attr_list.append(attribute)

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


    def set_fillcolor(self, color):

        self._fillcolor = color

        if isinstance(color, str):
            self._bg.set_property("fill-color", color)
        elif isinstance(color, int) or isinstance(color, long):
            self._bg.set_property("fill-color-rgba", color)
        else:
            log.debug("passing %s to set_linecolor", color)


    def get_icon_path(cls):

        filename = resource_filename('rascase.resources.pixmaps', 'entity-icon.png')
        return filename

    get_icon_path = staticmethod(get_icon_path) #makes the method static

    #get-set de propiedad
    def get_body(self):
        """Retorna el cuerpo del objeto

        """
        return self._body

    def set_title(self, name):
        self._name = "<b>" + name + "</b>"

    def refresh(self):
        print "nombre entidad:", self._name
        self._entity_title.set_property("text", self._name)
        self.translate(0,0) #trick to update the view

class AttributeComponent(gobject.GObject):
    "Componente gráfico que se pone dentro de una entidad"
    def __init__(self, name, datatype, default_value=None, pk=False, mandatory=False):
        gobject.GObject.__init__(self)
        self._name = name
        self._default_value = default_value
        self._mandatory = mandatory
        self._primary_key = pk
        self._data_type = datatype[0]

        if len(datatype) > 1:
            self._data_type_length = datatype[1]
        else:
            self._data_type_length = None

        self.items = {'mandatory':goocanvas.Text(text="", use_markup=True, font="sans 8"),
                      'name':goocanvas.Text(text="", use_markup=True, font="sans 8"),
                      'datatype':goocanvas.Text(text="", use_markup=True, font="sans 8")
                      }

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

    def refresh(self):
        mod = self.get_data("model")

        if mod.is_mandatory() != self._mandatory:
            self._mandatory = mod.is_mandatory()
            if self._mandatory:
                text_m = "[M]"
            else:
                text_m = ""
            self.items['mandatory'].set_property("text", text_m)

        self._name = mod.get_name()
        self._primary_key = mod.is_primary_key()
        if self._primary_key:
            text_name = "<u>" + self._name + "</u>"
        else:
            text_name = self._name

        self.items['name'].set_property("text", text_name)

        #FIXME: this should not happen, the controller must do this
        dt_changed = False
        if mod.get_data_type()[0] != self._data_type:
            self._data_type = mod.get_data_type()[0]
            dt_changed = True

        if (len(mod.get_data_type())>1):
            if mod.get_data_type()[1] != self._data_type_length:
                self._data_type_length = mod.get_data_type()[1]
                dt_changed = True
        else:
            self._data_type_length = None
            dt_changed = True
        if dt_changed:
            from rascase.core import LogicalDataType
            text_dt = LogicalDataType.to_string(self._data_type)
            if self._data_type_length != None:
                text_dt = text_dt + "(" + str(self._data_type_length) + ")"

            self.items['datatype'].set_property("text", text_dt)

        #trick to update the view
        for key in self.items.keys():
            self.items[key].translate(0,0)

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
    __gsignals__ = {
        'on-double-click': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ())
        }

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

    def set_line_color(self, value):

        if isinstance(value,str):
            self.set_property("stroke-color", value)
        else:
            self.set_property("stroke-color-rgba", value)

        self._line_color = value

    def get_line_color(self):
        return self._line_color

class RelationshipComponent(LineBaseComponent):
    def __init__(self, entity1, dependent1, mandatory1,
                 entity2, dependent2, mandatory2, cardinality, color):

        #entity 1
        self._entity1 = entity1
        self._dependent1 = dependent1
        self._mandatory1 = mandatory1

        #entity 2
        self._entity2 = entity2
        self._dependent2 = dependent2
        self._mandatory2 = mandatory2

        #cardinality
        self._cardinality = cardinality

        LineBaseComponent.__init__(self,
                                   can_focus=True,
                                   points=self._build_points(),
                                   stroke_color_rgba=color)

        # signals connections
        self._entity1.connect("on-movement",self._on_entity_movement)
        self._entity2.connect("on-movement",self._on_entity_movement)
        self.connect("button-press-event", self._on_button_press)
        self.connect("focus-in-event", self._on_focus_in)
        self.connect("focus-out-event", self._on_focus_out)


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

        #starts variations

        from rascase.core import Relationship

        if self._entity1.get_x() < self._entity2.get_x():
            if self._cardinality == Relationship.CARDINALITY_1_N or \
                   self._cardinality == Relationship.CARDINALITY_1_1:
                if self._dependent1:
                    p1 = (x1+5, y1)
                    points_list.append(p1)
                    points_list.append((p1[0]+10,p1[1]))
                    points_list += self._do_triangle((p1[0]+10,p1[1]), p1, False)
                    pf = p1
                else:
                    pf = (x1+15,y1)
                    points_list.append(pf)

            elif self._cardinality == Relationship.CARDINALITY_N_1 or \
                     self._cardinality == Relationship.CARDINALITY_N_N:
                if self._dependent1:
                    points_list += self._do_pata_triangle((x1,y1),
                                                          (x1+18,y1),
                                                          right=False)
                    pf = (x1+15, y1)

                else:
                    points_list += self._do_pata_gallo((x1+15, y1), (x1,y1))
                    pf = (x1+15, y1)

            if self._mandatory2:
                p1 = (pf[0]+10, pf[1])
                points_list.append(p1)
                points_list += self._do_line(p1)

            else:
                h = pf[0]+15
                k = pf[1]
                r = 5
                points_list += self._do_circle(h, k, r)

        else:
            pass

        #finish variations

        points_list.append((x2,y2))

        pts = goocanvas.Points(points_list)
        return pts

    def _one(self, pt_begin, pt_end):
        pts = list()
        if pt_begin[0] < pt_end[0]:
            #entity 1 is on the left
            dif = pt_end[0] - pt_begin[0]
            p1 = (pt_begin[0]+dif/4, pt_begin[1])
            pts.append(p1)

            if self._mandatory2:
                # draw a vertical line
                pts += self._do_line(p1)
            else:
                # draw a little circle
                # (x-h)^2 + (y-k)^2 = r^2
                r = 5
                h = p1[0]+5
                k = p1[1]
                pts += self._do_circle(h, k, r)
        else:
            #entity 1 is on the right
            dif = pt_begin[0] - pt_end[0]
            p1 = (pt_begin[0]-dif/4, pt_begin[1])
            pts.append(p1)

            if self._mandatory2:
                # draw vertical line
                pts += self._do_line(p1)

            else:
                # draw a little circle
                # (x-h)^2 + (y-k)^2 = r^2
                r = 5
                h = p1[0]-5
                k = p1[1]
                pts += self._do_circle(h, k, r)

        pts.append(pt_end)
        return pts

    def _do_line(self, p1):
        pts = list()

        p2 = (p1[0], p1[1] - 10)
        pts.append(p2)

        p3 = (p1[0], p1[1] + 10)
        pts.append(p3)
        pts.append(p1)
        return pts

    def _do_circle(self, h, k, r):
        pts = list()
        x = h-r
        while x < h+r:
            y = math.sqrt(25-math.pow(x-h,2))+k
            pts.append((x,y))
            x+=0.2 # the step

        x = h-r
        while x < h+r:
            y = -math.sqrt(25-math.pow(x-h,2))+k
            pts.append((x,y))
            x+=0.2 # the step

        return pts

    def _do_triangle(self, pt_begin, pt_end, left_at_end=True):
        pts = list()
        if pt_begin[0] < pt_end[0]:
            #  /|
            #  \|
            p1 = (pt_begin[0]+10, pt_begin[1]-10)
            pts.append(p1)

            p2 = (p1[0], p1[1]+20)
            pts.append(p2)
            pts.append(pt_begin)
            if left_at_end:
                pts.append(p2)

                p3 = (p2[0], p2[1]-10)
                pts.append(p3)
        else:
            # |\
            # |/
            p1 = (pt_begin[0]-10, pt_begin[1]-10)
            pts.append(p1)

            p2 = (p1[0], p1[1]+20)
            pts.append(p2)
            pts.append(pt_begin)

            if left_at_end:
                pts.append(p2)

                p3 = (p2[0], p2[1]-10)
                pts.append(p3)

        return pts

    def _do_pata_triangle(self, pt_begin, pt_end, right=True):
        pts = list()

        if right:
            #    /|-
            # -<  |-
            #    \|-
            p0 = (pt_end[0]-5, pt_end[1])
            pts += self._do_triangle(pt_begin, p0)
            p1 = (p0[0], p0[1]-3)
            pts.append(p1)

            p2 = (p1[0]+5, p1[1])
            pts.append(p2)
            pts.append(p1)

            p3 = (p1[0], p1[1]+6)
            pts.append(p3)

            p4 = (p3[0]+5, p3[1])
            pts.append(p4)
            pts.append(p3)
            pts.append(p0)
            pts.append(pt_end)

        else:
            # -|\
            # -| >-
            # -|/
            p0 = (pt_begin[0]+8, pt_begin[1])
            pts.append(p0)

            p1 = (p0[0], p0[1]-5)
            pts.append(p1)

            p2 = (p1[0]-8, p1[1])
            pts.append(p2)
            pts.append(p1)

            p3 = (p1[0], p1[1]+10)
            pts.append(p3)

            p4 = (p3[0]-8, p3[1])
            pts.append(p4)
            pts.append(p3)
            pts.append(p0)
            pts.append(pt_end)
            pts += self._do_triangle(pt_end, p0, False)

        return pts

    def _do_pata_gallo(self, pt_begin, pt_end, left_at_end=True):

        pts = list()

        pts.append(pt_end)
        pts.append(pt_begin)

        p1 = (pt_end[0], pt_end[1]-5)
        pts.append(p1)
        pts.append(pt_begin)

        p2 = (pt_end[0], pt_end[1]+5)
        pts.append(p2)
        pts.append(pt_begin)

        if left_at_end:
            pts.append(pt_end)

        ## else:
        ##     #  \
        ##     # ---
        ##     #  /
        ##     pts.append(pt_end)

        return pts

    def set_cardinality(self, type_):
        self._cardinality = type_

    def get_cardinality(self):
        return self._cardinality

    def set_entity1(self, entity):
        self._entity1 = entity

    def get_entity1(self):
        return self._entity1

    def set_entity2(self, entity):
        self._entity2 = entity

    def get_entity2(self):
        return self._entity2

    #signal callbacks
    def _on_entity_movement(self, item):
        "Este metodo es ejecutado cada vez que alguna de las entidades de la relacion emite la señal 'on-movement'"
        self.set_property("points", self._build_points())

    def _on_button_press(self, item, target_item, event):
        if event.type == gtk.gdk._2BUTTON_PRESS:
            self.emit("on-double-click")
            print "double click"

        canvas = item.get_canvas()
        canvas.grab_focus(item)

    def _on_focus_in(self, item, target_item, event):
        self.set_line_color(TANGO_COLOR_ORANGE_DARK)

    def _on_focus_out(self, item, target_item, event):
        self.set_line_color(int('000000ff',16))

class InheritanceComponent(LineBaseComponent):
    def __init__(self, father, son, **kargs):

        self._father = father
        self._son = son
        LineBaseComponent.__init__(self,
                                   points=self._build_points(),
                                   stroke_color="green")

        self._father.connect("on-movement", self._on_entity_movement)
        self._son.connect("on-movement", self._on_entity_movement)

    def _build_points(self):
        points_list = list()

        if self._father.get_x() < self._son.get_x():
            x1 = self._father.get_x() + self._father.get_width()
            x2 = self._son.get_x()
        else:
            x1 = self._father.get_x()# - self._father.get_width()
            x2 = self._son.get_x() + self._son.get_width()

        y1 = self._father.get_y() + self._father.get_height()/2
        y2 = self._son.get_y() + self._son.get_height()/2

        points_list.append((x1,y1))

        if self._father.get_x() < self._son.get_x():
            p1 = (x2-15, y2)
            points_list.append(p1)

            p2 = (p1[0] + 5, p1[1])
            points_list.append(p2)

            p3 = (p2[0], p2[1] - 10)
            points_list.append(p3)

            p4 = (p3[0] + 10, p3[1] + 10)
            points_list.append(p4)

            p5 = (p4[0] - 10, p4[1] + 10)
            points_list.append(p5)

            points_list.append(p2)
        else:
            p1 = (x2 + 15, y2)
            points_list.append(p1)

            p2 = (p1[0] - 5, p1[1])
            points_list.append(p2)

            p3 = (p2[0], p2[1] - 10)
            points_list.append(p3)

            p4 = (p3[0] - 10, p3[1] + 10)
            points_list.append(p4)

            p5 = (p4[0] + 10, p4[1] + 10)
            points_list.append(p5)

            points_list.append(p2)

        #points_list.append((x2,y2))

        pts = goocanvas.Points(points_list)

        return pts

    def set_father(self, father):
        self._father = father

    def get_father(self):
        return self._father

    def set_son(self, son):
        self._son = son

    def get_son(self):
        return self._son

    def _on_entity_movement(self, item):
        self.set_property("points", self._build_points())

#physical model components

class TableComponent(RectBaseComponent):
    def __init__(self):
        RectBaseComponent.__init__(self)

class ReferenceComponent(LineBaseComponent):
    def __init__(self):
        LineBaseComponent.__init__(self)



class Canvas(goocanvas.Canvas):
    "Esta clase configura el canvas que provee goocanvas.Canvas"

    def __init__(self, **kargs):
        goocanvas.Canvas.__init__(self, **kargs)
        self.scrolled_win = gtk.ScrolledWindow()
        self.scrolled_win.set_shadow_type(gtk.SHADOW_IN)
        self.scrolled_win.set_data("canvas", self)
        self.scrolled_win.show()

        self.set_flags(gtk.CAN_FOCUS)
        self.set_size_request(640, 480)
        self.set_bounds(0, 0, 800, 700)
        root = self.get_root_item()
        self.set_root_item(root)
        self.show()

        self.scrolled_win.add(self)

    def add_child(self, item):
        self.get_root_item().add_child(item)

